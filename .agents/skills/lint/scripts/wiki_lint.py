#!/usr/bin/env python3
"""Deterministic lint for the llm-wiki repository."""

import argparse
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


DEFAULT_CATEGORIES = [
    "summaries",
    "entities",
    "concepts",
    "comparisons",
    "overviews",
    "syntheses",
    "recipes",
]


@dataclass
class WikiLink:
    target: str
    line: int


@dataclass
class Heading:
    level: int
    text: str
    line: int


@dataclass
class ParsedMarkdown:
    frontmatter: Dict[str, str]
    body: str
    wiki_links: List[WikiLink]
    headings: List[Heading]


@dataclass
class Issue:
    level: str
    path: str
    message: str


@dataclass
class Change:
    path: str
    message: str


@dataclass
class Report:
    changes: List[Change] = field(default_factory=list)
    issues: List[Issue] = field(default_factory=list)

    @property
    def fixed_count(self) -> int:
        return len(self.changes)


def split_frontmatter(text: str) -> Tuple[Dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[text.find("\n", end + 1) + 1 :]
    data: Dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def _strip_inline_code(line: str) -> str:
    out: List[str] = []
    in_code = False
    i = 0
    while i < len(line):
        if line[i] == "`":
            ticks = 1
            while i + ticks < len(line) and line[i + ticks] == "`":
                ticks += 1
            in_code = not in_code
            i += ticks
            continue
        if not in_code:
            out.append(line[i])
        i += 1
    return "".join(out)


def _strip_obsidian_comments(line: str, in_comment: bool) -> Tuple[str, bool]:
    out: List[str] = []
    i = 0
    while i < len(line):
        if line.startswith("%%", i):
            in_comment = not in_comment
            i += 2
            continue
        if not in_comment:
            out.append(line[i])
        i += 1
    return "".join(out), in_comment


def parse_markdown(text: str) -> ParsedMarkdown:
    frontmatter, body = split_frontmatter(text)
    links: List[WikiLink] = []
    headings: List[Heading] = []
    in_fence = False
    fence_marker = ""
    in_comment = False

    for line_no, line in enumerate(body.splitlines(), 1):
        stripped = line.lstrip()
        if not in_fence and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence = True
            fence_marker = stripped[:3]
            continue
        if in_fence:
            if stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            continue

        cleaned, in_comment = _strip_obsidian_comments(line, in_comment)
        cleaned = _strip_inline_code(cleaned)

        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", cleaned)
        if heading_match:
            headings.append(
                Heading(
                    level=len(heading_match.group(1)),
                    text=heading_match.group(2).strip(),
                    line=line_no,
                )
            )

        for match in re.finditer(r"!?\[\[([^\]]+)\]\]", cleaned):
            raw_target = match.group(1).split("|", 1)[0].split("#", 1)[0].strip()
            if raw_target:
                links.append(WikiLink(target=raw_target, line=line_no))

    return ParsedMarkdown(frontmatter=frontmatter, body=body, wiki_links=links, headings=headings)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_if_changed(path: Path, content: str, fix: bool, report: Report, message: str) -> None:
    old = read_text(path) if path.exists() else ""
    if old == content:
        return
    if fix:
        path.write_text(content, encoding="utf-8")
        report.changes.append(Change(str(path), message))
    else:
        report.issues.append(Issue("fixable", str(path), message))


def domain_dirs(root: Path) -> List[Path]:
    return sorted(
        p for p in root.iterdir() if p.is_dir() and (p / "domain.md").exists() and (p / "wiki").is_dir()
    )


def categories_for(domain: Path) -> List[str]:
    domain_md = domain / "domain.md"
    if not domain_md.exists():
        return DEFAULT_CATEGORIES[:]
    text = read_text(domain_md)
    section = text
    match = re.search(r"## 分类体系\n(?P<body>.*?)(?:\n## |\Z)", text, re.S)
    if match:
        section = match.group("body")
    cats = []
    for match in re.finditer(r"-\s+`([^`/]+)/`", section):
        cat = match.group(1).strip()
        if cat and cat not in cats:
            cats.append(cat)
    return cats or DEFAULT_CATEGORIES[:]


def wiki_pages(domain: Path) -> List[Path]:
    wiki = domain / "wiki"
    return sorted(
        p
        for p in wiki.rglob("*.md")
        if p.name not in {"index.md", "log.md"} and "notes" not in p.parts and "raw" not in p.parts
    )


def page_title(path: Path) -> str:
    return path.stem


def page_date(path: Path) -> Optional[str]:
    data, _ = split_frontmatter(read_text(path))
    date = data.get("date")
    return date if date else None


def parse_index_entries(text: str) -> Dict[str, Tuple[str, str]]:
    entries: Dict[str, Tuple[str, str]] = {}
    current = ""
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip().lower()
            continue
        entry = re.match(r"^-\s+\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]\s*(?:[—-]\s*(.*))?$", line)
        if entry:
            title = entry.group(1).strip()
            desc = (entry.group(2) or "待补充").strip()
            entries[title] = (current, desc)
    return entries


def render_index(domain: Path, categories: List[str], entries: Dict[str, Tuple[str, str]]) -> str:
    index_path = domain / "wiki" / "index.md"
    old = read_text(index_path) if index_path.exists() else ""
    frontmatter, _ = split_frontmatter(old)
    title = frontmatter.get("title") or f"{domain.name} Wiki 索引"
    date = frontmatter.get("date") or datetime.now().strftime("%Y-%m-%d")
    page_by_title = {page_title(path): path for path in wiki_pages(domain)}
    by_category: Dict[str, List[str]] = {cat: [] for cat in categories}
    extra_categories: List[str] = []

    for title_name, path in page_by_title.items():
        rel = path.relative_to(domain / "wiki")
        cat = rel.parts[0] if len(rel.parts) > 1 else "uncategorized"
        if cat not in by_category:
            by_category[cat] = []
            extra_categories.append(cat)
        by_category[cat].append(title_name)

    lines = [
        "---",
        f"title: {title}",
        f"date: {date}",
        "---",
        "",
        f"# {domain.name} Wiki 索引",
        "",
    ]

    for cat in categories + extra_categories:
        lines.append(f"## {cat}")
        lines.append("")
        ordered: List[str] = []
        for old_title, (old_cat, _) in entries.items():
            if old_cat == cat and old_title in by_category.get(cat, []):
                ordered.append(old_title)
        for title_name in sorted(by_category.get(cat, [])):
            if title_name not in ordered:
                ordered.append(title_name)
        if ordered:
            for title_name in ordered:
                desc = entries.get(title_name, ("", "待补充"))[1] or "待补充"
                lines.append(f"- [[{title_name}]] — {desc}")
        else:
            lines.append("_（暂无）_")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def normalize_domain_index(domain: Path, fix: bool, report: Report) -> None:
    index_path = domain / "wiki" / "index.md"
    if not index_path.exists():
        report.issues.append(Issue("error", str(index_path), "Missing wiki/index.md"))
        return
    old = read_text(index_path)
    entries = parse_index_entries(old)
    new = render_index(domain, categories_for(domain), entries)
    write_if_changed(index_path, new, fix, report, "normalized wiki/index.md")


def count_wiki_pages(domain: Path) -> int:
    return len(wiki_pages(domain))


def update_top_index(root: Path, fix: bool, report: Report) -> None:
    path = root / "index.md"
    if not path.exists():
        return
    content = read_text(path)
    new = content
    for domain in domain_dirs(root):
        count = count_wiki_pages(domain)
        pattern = rf"(\[\[{re.escape(domain.name)}/wiki/index\|{re.escape(domain.name)}\]\].*?（)\d+( 页）)"
        new = re.sub(pattern, rf"\g<1>{count}\2", new)
    write_if_changed(path, new, fix, report, "updated top-level page counts")


def page_map(domain: Path) -> Dict[str, Path]:
    return {page_title(path): path for path in wiki_pages(domain)}


def check_query_archives(domain: Path, report: Report) -> None:
    pages = page_map(domain)
    for path in wiki_pages(domain):
        doc = parse_markdown(read_text(path))
        if doc.frontmatter.get("type") != "query_archive":
            continue
        missing = []
        heading_names = {h.text for h in doc.headings}
        if "基于页面" not in heading_names:
            missing.append("## 基于页面")
        if "来源" not in heading_names:
            missing.append("## 来源")
        if doc.frontmatter.get("source_count") != "0":
            missing.append("source_count: 0")
        if missing:
            report.issues.append(Issue("warning", str(path), "Query archive missing " + ", ".join(missing)))

        archive_date = doc.frontmatter.get("date")
        if not archive_date:
            continue
        for link in doc.wiki_links:
            base = pages.get(link.target)
            if not base or base == path:
                continue
            base_date = page_date(base)
            if base_date and base_date > archive_date:
                report.issues.append(
                    Issue(
                        "warning",
                        str(path),
                        f"Query archive {page_title(path)} may be stale: {link.target} updated on {base_date} after archive date {archive_date}",
                    )
                )


def check_qmd_config(domain: Path, report: Report) -> None:
    text = read_text(domain / "domain.md")
    name = domain.name
    expected_root = f"collection root：`{name}/wiki`"
    if "索引路径：`./wiki/`" in text or "索引路径：./wiki/" in text:
        report.issues.append(Issue("warning", str(domain / "domain.md"), "deprecated qmd path: ./wiki/"))
    if "collection 名称" not in text:
        report.issues.append(Issue("warning", str(domain / "domain.md"), "missing qmd collection name"))
    if expected_root not in text:
        report.issues.append(Issue("warning", str(domain / "domain.md"), f"missing qmd collection root `{name}/wiki`"))
    if "collection 注册" not in text:
        report.issues.append(Issue("warning", str(domain / "domain.md"), "missing qmd collection registration rule"))


def qmd_config(domain: Path) -> Tuple[Optional[str], Optional[str]]:
    text = read_text(domain / "domain.md")
    collection = None
    root = None
    collection_match = re.search(r"collection 名称：`([^`]+)`", text)
    root_match = re.search(r"collection root：`([^`]+)`", text)
    if collection_match:
        collection = collection_match.group(1)
    if root_match:
        root = root_match.group(1)
    return collection, root


def parse_qmd_collection_list(output: str) -> Dict[str, int]:
    collections: Dict[str, int] = {}
    current: Optional[str] = None
    for line in output.splitlines():
        name_match = re.match(r"^(\S+)\s+\(qmd://", line)
        if name_match:
            current = name_match.group(1)
            collections[current] = -1
            continue
        files_match = re.match(r"^\s+Files:\s+(\d+)", line)
        if files_match and current:
            collections[current] = int(files_match.group(1))
    return collections


def parse_qmd_collection_path(output: str) -> Optional[str]:
    for line in output.splitlines():
        match = re.match(r"^\s+Path:\s+(.+?)\s*$", line)
        if match:
            return match.group(1)
    return None


def parse_qmd_collection_context_count(output: str) -> Optional[int]:
    for line in output.splitlines():
        match = re.match(r"^\s+Contexts:\s+(\d+)\s*$", line)
        if match:
            return int(match.group(1))
    return None


def parse_qmd_status(output: str) -> Dict[str, int]:
    status: Dict[str, int] = {}
    for line in output.splitlines():
        match = re.match(r"^\s+(Total|Vectors|Pending):\s+(\d+)", line)
        if match:
            status[match.group(1).lower()] = int(match.group(2))
    return status


def check_qmd_state(root: Path, domains: Iterable[Path], report: Report) -> None:
    if shutil.which("qmd") is None:
        return
    try:
        result = subprocess.run(
            ["qmd", "collection", "list"],
            cwd=str(root),
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError as exc:
        report.issues.append(Issue("warning", "qmd", f"qmd collection state unavailable: {exc}"))
        return
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).splitlines()[0] if (result.stderr or result.stdout) else "unknown error"
        report.issues.append(Issue("warning", "qmd", f"qmd collection state unavailable: {detail}"))
        return

    collections = parse_qmd_collection_list(result.stdout)
    status_result = subprocess.run(
        ["qmd", "status"],
        cwd=str(root),
        check=False,
        text=True,
        capture_output=True,
    )
    if status_result.returncode == 0:
        status = parse_qmd_status(status_result.stdout)
        pending = status.get("pending", 0)
        if pending > 0:
            report.issues.append(
                Issue(
                    "info",
                    "qmd",
                    f"qmd has {pending} documents pending embeddings; vsearch and hybrid query are not fully ready",
                )
            )

    for domain in domains:
        collection, collection_root = qmd_config(domain)
        if not collection or not collection_root:
            continue
        if collection not in collections:
            continue
        expected_files = len(list((domain / "wiki").rglob("*.md")))
        actual_files = collections.get(collection, -1)
        if actual_files != -1 and actual_files != expected_files:
            report.issues.append(
                Issue(
                    "warning",
                    collection,
                    f"qmd file count differs from wiki: {actual_files} indexed vs {expected_files} files; run qmd update",
                )
            )
        show = subprocess.run(
            ["qmd", "collection", "show", collection],
            cwd=str(root),
            check=False,
            text=True,
            capture_output=True,
        )
        if show.returncode != 0:
            continue
        actual_path = parse_qmd_collection_path(show.stdout)
        context_count = parse_qmd_collection_context_count(show.stdout)
        expected_path = str((root / collection_root).resolve())
        if actual_path and actual_path != expected_path:
            report.issues.append(
                Issue("warning", collection, f"qmd collection path is {actual_path}, expected {expected_path}")
            )
        if context_count == 0:
            report.issues.append(
                Issue("info", collection, "qmd collection has no root context; cross-collection disambiguation may be weaker")
            )


def lint_repo(root: Path, fix: bool = False) -> Report:
    report = Report()
    domains = domain_dirs(root)
    for domain in domains:
        normalize_domain_index(domain, fix, report)
        check_query_archives(domain, report)
        check_qmd_config(domain, report)
    update_top_index(root, fix, report)
    check_qmd_state(root, domains, report)
    return report


def format_report(report: Report) -> str:
    lines = ["# Wiki Lint Report", ""]
    lines.append(f"Deterministic fixes: {len(report.changes)}")
    for change in report.changes:
        lines.append(f"- FIXED {change.path}: {change.message}")
    lines.append("")
    lines.append(f"Findings: {len(report.issues)}")
    for issue in report.issues:
        lines.append(f"- {issue.level.upper()} {issue.path}: {issue.message}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="knowledge repository root")
    parser.add_argument("--fix", action="store_true", help="apply deterministic fixes")
    args = parser.parse_args()

    report = lint_repo(Path(args.root).resolve(), fix=args.fix)
    print(format_report(report))
    return 1 if any(issue.level == "error" for issue in report.issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
