#!/usr/bin/env python3
"""
Init-Domain automation script.
Creates directory structure, generates boilerplate files for a new domain,
and updates README.md when present.

Usage:
    python init-domain.py <domain_name> [options]

Options:
    --categories    Comma-separated list of wiki subdirectories (default: summaries,entities,concepts,comparisons,overviews,syntheses,recipes)
    --tags          Comma-separated list of initial tags
    --overview      Domain overview description (1-2 sentences)
    --output-dir    Output directory (default: current directory)

Example:
    python init-domain.py 投资 --categories summaries,entities,concepts,comparisons,overviews,syntheses,strategies,tracking \
        --tags value-investing,quantitative-trading,portfolio-management \
        --overview "价值投资、量化策略和市场分析"
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def create_directory_structure(base_dir: str, domain: str, categories: list[str]):
    """Create the complete directory structure for a new domain."""
    paths = [
        f"{base_dir}/{domain}/raw/articles",
        f"{base_dir}/{domain}/raw/papers",
        f"{base_dir}/{domain}/raw/books",
        f"{base_dir}/{domain}/raw/videos",
        f"{base_dir}/{domain}/raw/podcasts",
        f"{base_dir}/{domain}/raw/others",
        f"{base_dir}/{domain}/raw/archive",
        f"{base_dir}/{domain}/wiki",
        f"{base_dir}/{domain}/notes",
    ]
    for cat in categories:
        paths.append(f"{base_dir}/{domain}/wiki/{cat}")

    for p in paths:
        os.makedirs(p, exist_ok=True)
        # Create .gitkeep in all empty directories so Git tracks them
        if not os.listdir(p):
            open(f"{p}/.gitkeep", "a").close()

    return paths


def generate_domain_md(domain: str, overview: str, categories: list[str], tags: list[str]) -> str:
    """Generate the domain.md content."""
    today = datetime.now().strftime("%Y-%m-%d")
    cat_lines = "\n".join(f"- `{cat}/` — （请补充说明）" for cat in categories)
    tag_lines = "\n".join(f"- `#{t}` — （请补充说明）" for t in tags)
    collection = f"knowledge-{domain.lower()}"
    collection_root = f"{domain}/wiki"

    return f"""---
title: {domain} 领域规则
date: {today}
domain: {domain}
---

# {domain} 领域规则

## 领域概述

{overview}

## 分类体系

wiki 页面按以下子目录组织：

{cat_lines}

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

{tag_lines}

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`{collection}`
- collection root：`{collection_root}`
- collection 注册：由 `qmd_sync.py` 根据 Git 根目录与 collection root 幂等同步；本机配置不写入仓库

## 特殊约定

- （请根据领域特点补充）
"""


def generate_index_md(domain: str, categories: list[str]) -> str:
    """Generate the wiki/index.md content."""
    today = datetime.now().strftime("%Y-%m-%d")
    cat_sections = "\n\n".join(
        f"## {cat}\n\n_（暂无）_" for cat in categories
    )

    return f"""---
title: {domain} Wiki 索引
date: {today}
---

# {domain} Wiki 索引

{cat_sections}
"""


def generate_log_md(domain: str) -> str:
    """Generate the wiki/log.md content."""
    return f"""# {domain} Wiki 操作日志

"""


def update_readme_domains(base_dir: str, domain: str, overview: str) -> bool:
    """Upsert the domain in README.md's existing domains table."""
    readme_path = os.path.join(base_dir, "README.md")
    if not os.path.exists(readme_path):
        return False

    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    heading = "## 现有领域"
    start = content.find(heading)
    if start == -1:
        return False

    end = content.find("\n---", start)
    if end == -1:
        return False

    section = content[start:end]
    lines = section.splitlines()
    safe_overview = overview.replace("|", "\\|")
    row = f"| [{domain}]({domain}/wiki/index.md) | {safe_overview} | 活跃 |"

    updated = False
    last_domain_row = None
    for i, line in enumerate(lines):
        if line.startswith("| ["):
            last_domain_row = i
            if line.startswith(f"| [{domain}]("):
                if line != row:
                    lines[i] = row
                    updated = True
                break
    else:
        insert_at = (last_domain_row + 1) if last_domain_row is not None else len(lines)
        lines.insert(insert_at, row)
        updated = True

    if not updated:
        return False

    new_section = "\n".join(lines)
    new_content = content[:start] + new_section + content[end:]
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True


def update_top_index_domains(base_dir: str, domain: str, overview: str) -> bool:
    """Upsert the domain in knowledge/index.md, which is the routing source of truth."""
    index_path = os.path.join(base_dir, "index.md")
    today = datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(index_path):
        content = f"""---
title: 知识库领域目录
date: {today}
---

# 知识库领域目录

"""
    else:
        with open(index_path, encoding="utf-8") as f:
            content = f.read()

    safe_overview = overview.replace("\n", " ").strip()
    row = f"- [[{domain}/wiki/index|{domain}]] — {safe_overview}（0 页）"
    lines = content.rstrip().splitlines()
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"- [[{domain}/wiki/index|{domain}]]"):
            if line != row:
                lines[i] = row
                updated = True
            break
    else:
        if lines and lines[-1].startswith("# "):
            lines.append("")
        lines.append(row)
        updated = True

    if not updated:
        return False
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")
    return True


def diagnose_existing(domain_path: str, categories: list[str], base_dir: str, domain: str) -> dict:
    """Check an existing domain for missing files/directories and report issues."""
    issues = []
    created = []

    # Check raw/ subdirectories
    for sub in ["articles", "papers", "books", "videos", "podcasts", "others", "archive"]:
        p = os.path.join(domain_path, "raw", sub)
        if not os.path.isdir(p):
            os.makedirs(p, exist_ok=True)
            open(os.path.join(p, ".gitkeep"), "a").close()
            created.append(f"raw/{sub}/")

    # Check wiki/ subdirectories
    for cat in categories:
        p = os.path.join(domain_path, "wiki", cat)
        if not os.path.isdir(p):
            os.makedirs(p, exist_ok=True)
            open(os.path.join(p, ".gitkeep"), "a").close()
            created.append(f"wiki/{cat}/")

    # Check notes/
    notes_path = os.path.join(domain_path, "notes")
    if not os.path.isdir(notes_path):
        os.makedirs(notes_path, exist_ok=True)
        open(os.path.join(notes_path, ".gitkeep"), "a").close()
        created.append("notes/")

    # Check domain.md
    domain_rules_path = os.path.join(domain_path, "domain.md")
    if not os.path.exists(domain_rules_path):
        issues.append("Missing: domain.md")
    else:
        content = open(domain_rules_path, encoding="utf-8").read()
        if not content.strip().startswith("---"):
            issues.append("domain.md missing YAML frontmatter")
        required_sections = ["领域概述", "分类体系", "标签体系", "qmd 配置", "特殊约定"]
        for sec in required_sections:
            if sec not in content:
                issues.append(f"domain.md missing section: {sec}")
        if "索引路径：`./wiki/`" in content or "索引路径：./wiki/" in content:
            issues.append("domain.md uses deprecated qmd path: 索引路径：`./wiki/`; replace with collection root")
        expected_root = f"collection root：`{domain}/wiki`"
        if "collection root" not in content:
            issues.append(f"domain.md missing qmd collection root: `{domain}/wiki`")
        elif expected_root not in content:
            issues.append(f"domain.md qmd collection root should be `{domain}/wiki` relative to knowledge root")
        if "collection 注册" not in content:
            issues.append("domain.md missing qmd collection registration rule")

    # Check wiki/index.md
    index_path = os.path.join(domain_path, "wiki", "index.md")
    if not os.path.exists(index_path):
        issues.append("Missing: wiki/index.md")
    else:
        content = open(index_path, encoding="utf-8").read()
        if not content.strip().startswith("---"):
            issues.append("wiki/index.md missing YAML frontmatter")

    # Check wiki/log.md
    log_path = os.path.join(domain_path, "wiki", "log.md")
    if not os.path.exists(log_path):
        issues.append("Missing: wiki/log.md")

    return {"created": created, "issues": issues}


def sync_qmd_collection(base_dir: str, domain: str) -> None:
    """Best-effort local qmd registration; never blocks domain initialization."""
    script = Path(__file__).resolve().with_name("qmd_sync.py")
    if not script.exists():
        print("qmd-sync skipped: helper script not found")
        return
    completed = subprocess.run(
        [sys.executable, str(script), "--root", base_dir, "--apply", "--domain", domain],
        check=False,
        text=True,
        capture_output=True,
    )
    output = (completed.stdout or completed.stderr).strip()
    if output:
        print(f"\n{output}")
    if completed.returncode != 0:
        print("qmd-sync did not complete; domain files were still initialized successfully")


def main():
    parser = argparse.ArgumentParser(description="Initialize or repair a domain for the knowledge base")
    parser.add_argument("domain", help="Domain name (e.g., 心理学, 投资, AI)")
    parser.add_argument("--categories", default="summaries,entities,concepts,comparisons,overviews,syntheses,recipes",
                        help="Comma-separated wiki subdirectories")
    parser.add_argument("--tags", default="",
                        help="Comma-separated initial tags")
    parser.add_argument("--overview", default="",
                        help="Domain overview description")
    parser.add_argument("--output-dir", default=".",
                        help="Output directory")
    parser.add_argument("--check-existing", action="store_true",
                        help="If domain exists, diagnose and repair missing files instead of exiting")
    parser.add_argument("--skip-qmd-sync", action="store_true",
                        help="Do not reconcile this domain with local qmd configuration")

    args = parser.parse_args()

    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    base_dir = os.path.abspath(args.output_dir)
    domain = args.domain
    domain_path = f"{base_dir}/{domain}"
    existing = os.path.exists(domain_path)

    if existing and not args.check_existing:
        print(f"Error: Domain '{domain}' already exists at {domain_path}")
        print("Use --check-existing to diagnose and repair missing files")
        sys.exit(1)

    # Create directories (works for both new and existing domains)
    create_directory_structure(base_dir, domain, categories)
    print(f"{'Verified' if existing else 'Created'} directory structure for '{domain}'")

    # Generate files
    overview = args.overview or f"{domain} 领域的知识积累"
    domain_md = generate_domain_md(domain, overview, categories, tags)
    index_md = generate_index_md(domain, categories)
    log_md = generate_log_md(domain)

    # Only write files if they don't already exist (never overwrite)
    domain_rules_path = f"{domain_path}/domain.md"
    if not os.path.exists(domain_rules_path):
        with open(domain_rules_path, "w") as f:
            f.write(domain_md)
        print(f"Generated {domain}/domain.md")
    else:
        print(f"Preserved existing {domain}/domain.md")

    index_path = f"{domain_path}/wiki/index.md"
    if not os.path.exists(index_path):
        with open(index_path, "w") as f:
            f.write(index_md)
        print(f"Generated {domain}/wiki/index.md")
    else:
        print(f"Preserved existing {domain}/wiki/index.md")

    log_path = f"{domain_path}/wiki/log.md"
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write(log_md)
        print(f"Generated {domain}/wiki/log.md")
    else:
        print(f"Preserved existing {domain}/wiki/log.md")

    if update_readme_domains(base_dir, domain, overview):
        print(f"Updated README.md domain table for {domain}")
    if update_top_index_domains(base_dir, domain, overview):
        print(f"Updated index.md domain route for {domain}")

    # Diagnose if domain already existed
    if existing:
        diag = diagnose_existing(domain_path, categories, base_dir, domain)
        if diag["created"]:
            print(f"\nCreated missing directories: {', '.join(diag['created'])}")
        if diag["issues"]:
            print(f"\nDiagnosis: found {len(diag['issues'])} issue(s) in existing domain:")
            for issue in diag["issues"]:
                print(f"  - {issue}")
        else:
            print("\nDiagnosis: no issues found, domain is complete")

    if not args.skip_qmd_sync:
        sync_qmd_collection(base_dir, domain)

    print(f"\nDomain '{domain}' {'repaired' if existing else 'initialized'} successfully at {domain_path}")
    print(f"Wiki categories: {', '.join(categories)}")
    print(f"Initial tags: {', '.join(tags) or '(none)'}")


if __name__ == "__main__":
    main()
