#!/usr/bin/env python3
"""
Init-Domain automation script.
Creates directory structure and generates boilerplate files for a new domain.

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
import sys
from datetime import datetime


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
        # Create .gitkeep in empty directories
        if "raw/" in p or p.endswith("/notes"):
            open(f"{p}/.gitkeep", "a").close()

    return paths


def generate_claude_md(domain: str, overview: str, categories: list[str], tags: list[str]) -> str:
    """Generate the domain CLAUDE.md content."""
    today = datetime.now().strftime("%Y-%m-%d")
    cat_lines = "\n".join(f"- `{cat}/` — （请补充说明）" for cat in categories)
    tag_lines = "\n".join(f"- `#{t}` — （请补充说明）" for t in tags)

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

- collection 名称：`knowledge-{domain.lower()}`
- 索引路径：`./wiki/`

## 特殊约定

- （请根据领域特点补充）
"""


def generate_index_md(domain: str, categories: list[str]) -> str:
    """Generate the wiki/index.md content."""
    today = datetime.now().strftime("%Y-%m-%d")
    cat_sections = "\n\n".join(
        f"## {cat.capitalize()}\n\n_（暂无）_" for cat in categories
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
    today = datetime.now().strftime("%Y-%m-%d")

    return f"""# {domain} Wiki 操作日志

## [{today}] init-domain | 领域初始化
- 创建领域目录结构
- 生成领域 CLAUDE.md
"""


def diagnose_existing(domain_path: str, categories: list[str]) -> dict:
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
            created.append(f"wiki/{cat}/")

    # Check notes/
    notes_path = os.path.join(domain_path, "notes")
    if not os.path.isdir(notes_path):
        os.makedirs(notes_path, exist_ok=True)
        open(os.path.join(notes_path, ".gitkeep"), "a").close()
        created.append("notes/")

    # Check CLAUDE.md
    claude_path = os.path.join(domain_path, "CLAUDE.md")
    if not os.path.exists(claude_path):
        issues.append("Missing: CLAUDE.md")
    else:
        content = open(claude_path, encoding="utf-8").read()
        if not content.strip().startswith("---"):
            issues.append("CLAUDE.md missing YAML frontmatter")
        required_sections = ["领域概述", "分类体系", "标签体系", "qmd 配置", "特殊约定"]
        for sec in required_sections:
            if sec not in content:
                issues.append(f"CLAUDE.md missing section: {sec}")

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
    claude_md = generate_claude_md(domain, overview, categories, tags)
    index_md = generate_index_md(domain, categories)
    log_md = generate_log_md(domain)

    # Only write files if they don't already exist (never overwrite)
    claude_path = f"{domain_path}/CLAUDE.md"
    if not os.path.exists(claude_path):
        with open(claude_path, "w") as f:
            f.write(claude_md)
        print(f"Generated {domain}/CLAUDE.md")
    else:
        print(f"Preserved existing {domain}/CLAUDE.md")

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

    # Diagnose if domain already existed
    if existing:
        diag = diagnose_existing(domain_path, categories)
        if diag["created"]:
            print(f"\nCreated missing directories: {', '.join(diag['created'])}")
        if diag["issues"]:
            print(f"\nDiagnosis: found {len(diag['issues'])} issue(s) in existing domain:")
            for issue in diag["issues"]:
                print(f"  - {issue}")
        else:
            print("\nDiagnosis: no issues found, domain is complete")

    print(f"\nDomain '{domain}' {'repaired' if existing else 'initialized'} successfully at {domain_path}")
    print(f"Wiki categories: {', '.join(categories)}")
    print(f"Initial tags: {', '.join(tags) or '(none)'}")


if __name__ == "__main__":
    main()
