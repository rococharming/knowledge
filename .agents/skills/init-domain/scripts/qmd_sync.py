#!/usr/bin/env python3
"""Reconcile qmd collections with portable declarations in domain.md files.

`--check` is read-only. `--apply` creates missing collections and root
contexts, but never repairs path conflicts. By default an apply runs `qmd
update` only when configuration changed; `--refresh` forces one text-index
update after reconciliation for workflows that changed wiki files. The
explicit `--semantic` option provisions pinned local models and runs embed.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional


@dataclass(frozen=True)
class DomainConfig:
    domain: str
    collection: str
    root_relative: str
    root_absolute: str
    context: str


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    domain: str
    collection: str
    message: str


Runner = Callable[[list[str], Path], CommandResult]


def run_command(args: list[str], cwd: Path) -> CommandResult:
    completed = subprocess.run(
        args,
        cwd=str(cwd),
        check=False,
        text=True,
        capture_output=True,
    )
    return CommandResult(completed.returncode, completed.stdout, completed.stderr)


def repository_root(explicit: Optional[str] = None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode == 0 and completed.stdout.strip():
        return Path(completed.stdout.strip()).resolve()
    return Path.cwd().resolve()


def extract_context(text: str, domain: str) -> str:
    match = re.search(r"^## 领域概述\s*$\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return f"{domain} 领域知识库"
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", match.group(1)) if part.strip()]
    if not paragraphs:
        return f"{domain} 领域知识库"
    return re.sub(r"\s+", " ", paragraphs[0])


def load_domain_configs(root: Path, domains: Optional[Iterable[str]] = None) -> tuple[list[DomainConfig], list[Finding]]:
    root = root.resolve()
    selected = set(domains or [])
    configs: list[DomainConfig] = []
    findings: list[Finding] = []
    found_domains: set[str] = set()

    for domain_md in sorted(root.glob("*/domain.md")):
        domain = domain_md.parent.name
        if selected and domain not in selected:
            continue
        found_domains.add(domain)
        text = domain_md.read_text(encoding="utf-8")
        collection_match = re.search(r"collection 名称：`([^`]+)`", text)
        root_match = re.search(r"collection root：`([^`]+)`", text)
        if not collection_match or not root_match:
            findings.append(
                Finding("error", "invalid_declaration", domain, "", f"{domain}/domain.md 缺少 qmd collection 声明")
            )
            continue

        root_relative = root_match.group(1).strip()
        relative_path = Path(root_relative)
        root_absolute = (root / relative_path).resolve()
        try:
            root_absolute.relative_to(root)
        except ValueError:
            findings.append(
                Finding("error", "unsafe_root", domain, collection_match.group(1), f"collection root 越出仓库：{root_relative}")
            )
            continue
        if relative_path.is_absolute():
            findings.append(
                Finding("error", "absolute_root", domain, collection_match.group(1), f"collection root 必须是相对路径：{root_relative}")
            )
            continue
        if not root_absolute.is_dir():
            findings.append(
                Finding("error", "missing_root", domain, collection_match.group(1), f"collection root 不存在：{root_absolute}")
            )
            continue

        configs.append(
            DomainConfig(
                domain=domain,
                collection=collection_match.group(1),
                root_relative=root_relative,
                root_absolute=str(root_absolute),
                context=extract_context(text, domain),
            )
        )

    for domain in sorted(selected - found_domains):
        findings.append(Finding("error", "unknown_domain", domain, "", f"找不到领域：{domain}"))

    return configs, findings


def parse_collection_list(output: str) -> set[str]:
    collections: set[str] = set()
    for line in output.splitlines():
        match = re.match(r"^(\S+)\s+\(qmd://", line)
        if match:
            collections.add(match.group(1))
    return collections


def parse_collection_path(output: str) -> Optional[str]:
    for line in output.splitlines():
        match = re.match(r"^\s+Path:\s+(.+?)\s*$", line)
        if match:
            return str(Path(match.group(1)).expanduser().resolve())
    return None


def parse_context_count(output: str) -> Optional[int]:
    for line in output.splitlines():
        match = re.match(r"^\s+Contexts:\s+(\d+)\s*$", line)
        if match:
            return int(match.group(1))
    return None


def command_error(result: CommandResult) -> str:
    detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
    return detail.splitlines()[0]


def synchronize(
    root: Path,
    mode: str,
    domains: Optional[Iterable[str]] = None,
    refresh: bool = False,
    runner: Runner = run_command,
) -> dict:
    root = root.resolve()
    configs, findings = load_domain_configs(root, domains)
    changed = False
    updated = False

    listed = runner(["qmd", "collection", "list"], root)
    if listed.returncode != 0:
        findings.append(Finding("error", "qmd_unavailable", "", "", f"无法读取 qmd collection：{command_error(listed)}"))
        return build_result(findings, changed, updated)
    collections = parse_collection_list(listed.stdout)

    for config in configs:
        if config.collection not in collections:
            if mode == "check":
                findings.append(
                    Finding("info", "missing_collection", config.domain, config.collection, "collection 尚未在本机注册")
                )
                continue
            added = runner(
                ["qmd", "collection", "add", config.root_absolute, "--name", config.collection, "--mask", "**/*.md"],
                root,
            )
            if added.returncode != 0:
                findings.append(
                    Finding("error", "add_failed", config.domain, config.collection, f"collection 注册失败：{command_error(added)}")
                )
                continue
            context_added = runner(
                ["qmd", "context", "add", f"qmd://{config.collection}/", config.context],
                root,
            )
            if context_added.returncode != 0:
                findings.append(
                    Finding("error", "context_failed", config.domain, config.collection, f"根 context 添加失败：{command_error(context_added)}")
                )
            changed = True
            findings.append(Finding("fixed", "collection_added", config.domain, config.collection, "已注册 collection"))
            collections.add(config.collection)
            continue

        shown = runner(["qmd", "collection", "show", config.collection], root)
        if shown.returncode != 0:
            findings.append(
                Finding("error", "show_failed", config.domain, config.collection, f"无法读取 collection：{command_error(shown)}")
            )
            continue
        actual_path = parse_collection_path(shown.stdout)
        if actual_path and actual_path != config.root_absolute:
            findings.append(
                Finding(
                    "warning",
                    "path_conflict",
                    config.domain,
                    config.collection,
                    f"路径冲突：当前 {actual_path}，期望 {config.root_absolute}；未自动覆盖",
                )
            )
            continue
        context_count = parse_context_count(shown.stdout)
        # qmd omits the Contexts line entirely when a collection has none.
        if context_count in (None, 0):
            if mode == "check":
                findings.append(Finding("info", "missing_context", config.domain, config.collection, "缺少根 context"))
            else:
                context_added = runner(
                    ["qmd", "context", "add", f"qmd://{config.collection}/", config.context],
                    root,
                )
                if context_added.returncode != 0:
                    findings.append(
                        Finding("error", "context_failed", config.domain, config.collection, f"根 context 添加失败：{command_error(context_added)}")
                    )
                else:
                    changed = True
                    findings.append(Finding("fixed", "context_added", config.domain, config.collection, "已添加根 context"))

    blocking = any(f.level == "error" or f.code == "path_conflict" for f in findings)
    if mode == "apply" and not blocking and (changed or refresh):
        update = runner(["qmd", "update"], root)
        if update.returncode != 0:
            findings.append(Finding("error", "update_failed", "", "", f"qmd update 失败：{command_error(update)}"))
        else:
            updated = True
            findings.append(Finding("fixed", "index_updated", "", "", "已更新 qmd 文本索引"))

    return build_result(findings, changed, updated)


def build_result(findings: list[Finding], changed: bool, updated: bool) -> dict:
    has_error = any(f.level == "error" for f in findings)
    has_conflict = any(f.code == "path_conflict" for f in findings)
    needs_sync = any(f.code in {"missing_collection", "missing_context"} for f in findings)
    if has_error:
        status = "error"
        exit_code = 2
    elif has_conflict:
        status = "conflict"
        exit_code = 2
    elif needs_sync:
        status = "needs_sync"
        exit_code = 1
    elif changed:
        status = "changed"
        exit_code = 0
    else:
        status = "ok"
        exit_code = 0
    return {
        "status": status,
        "exit_code": exit_code,
        "changed": changed,
        "updated": updated,
        "findings": [asdict(finding) for finding in findings],
    }


def print_human(result: dict) -> None:
    print(f"qmd-sync: {result['status']}")
    if not result["findings"]:
        print("- collection 配置已同步，无需修改")
        return
    for finding in result["findings"]:
        scope = finding["collection"] or finding["domain"] or "qmd"
        print(f"- {finding['level'].upper()} {scope}: {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize qmd collections from domain.md declarations")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="Read-only collection and context check")
    modes.add_argument("--apply", action="store_true", help="Create missing collections and root contexts")
    parser.add_argument("--refresh", action="store_true", help="With --apply, run one qmd update even if config is unchanged")
    parser.add_argument(
        "--semantic",
        action="store_true",
        help="With --apply, provision pinned local semantic models and run qmd embed",
    )
    parser.add_argument("--domain", action="append", help="Limit to a domain directory name; may be repeated")
    parser.add_argument("--root", help="Knowledge repository root; defaults to git root")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()

    if args.refresh and not args.apply:
        parser.error("--refresh requires --apply")
    if args.semantic and not args.apply:
        parser.error("--semantic requires --apply")

    root = repository_root(args.root)
    if shutil.which("qmd") is None:
        result = {"status": "skipped", "exit_code": 0, "changed": False, "updated": False, "findings": []}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print("qmd-sync: skipped（未安装 qmd）")
        return 0

    result = synchronize(root, "apply" if args.apply else "check", args.domain, args.refresh)
    if args.semantic and result["exit_code"] == 0:
        semantic_script = Path(__file__).with_name("qmd_semantic.py")
        semantic = subprocess.run(
            [sys.executable, str(semantic_script), "--apply", "--embed", "--doctor", "--json"],
            cwd=str(root),
            check=False,
            text=True,
            capture_output=True,
        )
        try:
            semantic_result = json.loads(semantic.stdout)
        except json.JSONDecodeError:
            detail = semantic.stderr.strip() or semantic.stdout.strip() or "unknown error"
            result["findings"].append(
                asdict(Finding("error", "semantic_failed", "", "", f"语义环境配置失败：{detail.splitlines()[0]}"))
            )
            result["status"] = "error"
            result["exit_code"] = 2
        else:
            for item in semantic_result.get("findings", []):
                result["findings"].append(
                    asdict(
                        Finding(
                            item.get("level", "info"),
                            f"semantic_{item.get('code', 'unknown')}",
                            "",
                            "",
                            item.get("message", "qmd 语义环境状态已更新"),
                        )
                    )
                )
            if semantic.returncode != 0:
                result["status"] = "error"
                result["exit_code"] = 2
            elif result["status"] == "ok" and semantic_result.get("changed"):
                result["status"] = "changed"
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print_human(result)
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
