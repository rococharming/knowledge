#!/usr/bin/env python3
"""Smoke tests for the LLM Wiki ingest/query/lint skills.

The tests use temporary domains and a fake qmd binary, so they do not modify the
real knowledge wiki or the real qmd index.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
INGEST_SKILL = REPO_ROOT / ".agents/skills/ingest/SKILL.md"
QUERY_SKILL = REPO_ROOT / ".agents/skills/query/SKILL.md"
LINT_SKILL = REPO_ROOT / ".agents/skills/lint/SKILL.md"
CHECK_DOMAIN = REPO_ROOT / ".agents/skills/ingest/scripts/check-domain.sh"
POST_INGEST = REPO_ROOT / ".agents/skills/ingest/scripts/post-ingest.sh"


def run(cmd: list[str], *, cwd: Path = REPO_ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)


def assert_ok(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode != 0:
        raise AssertionError(f"{label} failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_domain(root: Path, name: str, *, custom: bool = False, pages: int = 3, index_lines: int = 20) -> Path:
    domain = root / name
    raw_dirs = ["articles", "papers", "books", "videos", "podcasts", "others", "archive"]
    wiki_dirs = ["summaries", "entities", "concepts", "comparisons", "overviews", "syntheses", "recipes"]
    if custom:
        wiki_dirs += ["snippets", "patterns", "projects"]

    for directory in raw_dirs:
        (domain / "raw" / directory).mkdir(parents=True, exist_ok=True)
    for directory in wiki_dirs:
        (domain / "wiki" / directory).mkdir(parents=True, exist_ok=True)
    (domain / "notes").mkdir(parents=True, exist_ok=True)

    categories = "\n".join(f"- `{d}/` — {d}" for d in wiki_dirs)
    write(
        domain / "CLAUDE.md",
        f"""---
title: {name} 领域规则
date: 2026-05-10
---

# {name} 领域规则

## 分类体系

{categories}

## qmd 配置

- collection 名称：`knowledge-{name.lower()}`
- 索引路径：`./wiki/`
""",
    )
    index_entries = "\n".join(f"- [[Page{i}]] — page {i}" for i in range(pages))
    filler = "\n".join(f"<!-- filler {i} -->" for i in range(index_lines))
    write(domain / "wiki/index.md", f"# {name} Wiki 索引\n\n{index_entries}\n\n{filler}\n")
    write(domain / "wiki/log.md", "# log\n")
    for i in range(pages):
        write(
            domain / "wiki/concepts" / f"Page{i}.md",
            f"---\ntitle: Page{i}\ndate: 2026-05-10\ntags: [test]\nsource_count: 1\n---\n\n# Page{i}\n",
        )
    return domain


def expected_query_mode(domain_count: int, page_count: int, index_lines: int) -> str:
    if domain_count >= 5 or page_count >= 200 or index_lines >= 500:
        return "qmd"
    return "index"


def make_fake_qmd(bin_dir: Path, state_dir: Path) -> Path:
    qmd = bin_dir / "qmd"
    write(
        qmd,
        r'''#!/usr/bin/env bash
set -u
LOG="${QMD_FAKE_LOG:?}"
COLLECTIONS="${QMD_FAKE_COLLECTIONS:?}"
cmd="${1:-}"
sub="${2:-}"

if [[ "$cmd" == "collection" && "$sub" == "list" ]]; then
  cat "$COLLECTIONS"
  exit 0
fi

if [[ "$cmd" == "collection" && "$sub" == "add" ]]; then
  path="$3"
  name=""
  while [[ $# -gt 0 ]]; do
    if [[ "$1" == "--name" ]]; then
      shift
      name="$1"
    fi
    shift || true
  done
  echo "collection-add $name $path" >> "$LOG"
  echo "$name (qmd://$name/)" >> "$COLLECTIONS"
  exit 0
fi

if [[ "$cmd" == "update" ]]; then
  echo "update" >> "$LOG"
  if [[ "${QMD_FAKE_UPDATE_FAIL:-0}" == "1" ]]; then
    echo "fake update failure" >&2
    exit 2
  fi
  echo "✓ All collections updated."
  exit 0
fi

if [[ "$cmd" == "status" ]]; then
  echo "Documents"
  echo "  Vectors: ${QMD_FAKE_VECTORS:-0} embedded"
  echo "  Pending: ${QMD_FAKE_PENDING:-0} need embedding"
  if [[ "${QMD_FAKE_NO_GPU:-0}" == "1" ]]; then
    echo "  GPU: none"
  fi
  exit 0
fi

if [[ "$cmd" == "search" || "$cmd" == "vsearch" || "$cmd" == "query" ]]; then
  echo "$cmd ${*:2}" >> "$LOG"
  printf '[{"file":"qmd://knowledge-smallwiki/concepts/page0.md","title":"Page0","score":0.9}]'
  exit 0
fi

if [[ "$cmd" == "embed" ]]; then
  echo "embed" >> "$LOG"
  exit 0
fi

echo "unsupported fake qmd command: $*" >&2
exit 64
''',
    )
    qmd.chmod(0o755)
    return qmd


def test_scale_decision() -> None:
    assert expected_query_mode(2, 10, 40) == "index"
    assert expected_query_mode(2, 200, 40) == "qmd"
    assert expected_query_mode(2, 10, 500) == "qmd"
    assert expected_query_mode(5, 10, 40) == "qmd"


def test_check_domain_custom_categories(tmp: Path) -> None:
    domain = make_domain(tmp, "CustomWiki", custom=True)
    result = run(["bash", str(CHECK_DOMAIN), str(domain)])
    assert_ok(result, "check-domain custom categories")
    for expected in ["snippets:", "patterns:", "projects:"]:
        if expected not in result.stdout:
            raise AssertionError(f"check-domain did not report custom category {expected}\n{result.stdout}")


def test_post_ingest_qmd_cases(tmp: Path) -> None:
    domain = make_domain(tmp, "SmallWiki", pages=3, index_lines=20)
    base_path = "/usr/bin:/bin:/usr/sbin:/sbin"

    missing = run(["bash", str(POST_INGEST), str(domain)], env={**os.environ, "PATH": base_path})
    assert_ok(missing, "post-ingest without qmd")
    if "qmd 未安装，跳过索引更新" not in missing.stdout:
        raise AssertionError(missing.stdout)

    fake_bin = tmp / "bin"
    fake_state = tmp / "qmd-state"
    fake_bin.mkdir()
    fake_state.mkdir()
    make_fake_qmd(fake_bin, fake_state)
    log = fake_state / "qmd.log"
    collections = fake_state / "collections.txt"
    log.write_text("", encoding="utf-8")
    collections.write_text("", encoding="utf-8")
    fake_env = {
        **os.environ,
        "PATH": f"{fake_bin}:{base_path}",
        "QMD_FAKE_LOG": str(log),
        "QMD_FAKE_COLLECTIONS": str(collections),
        "QMD_FAKE_PENDING": "7",
        "QMD_FAKE_NO_GPU": "1",
    }

    created = run(["bash", str(POST_INGEST), str(domain)], env=fake_env)
    assert_ok(created, "post-ingest creates missing collection")
    qmd_log = log.read_text(encoding="utf-8")
    if "collection-add knowledge-smallwiki" not in qmd_log or "update" not in qmd_log:
        raise AssertionError(qmd_log)
    if "7 个文档需要 embedding" not in created.stdout:
        raise AssertionError(created.stdout)

    log.write_text("", encoding="utf-8")
    existing = run(["bash", str(POST_INGEST), str(domain)], env=fake_env)
    assert_ok(existing, "post-ingest existing collection")
    qmd_log = log.read_text(encoding="utf-8")
    if "collection-add" in qmd_log or "update" not in qmd_log:
        raise AssertionError(qmd_log)

    failing = run(["bash", str(POST_INGEST), str(domain)], env={**fake_env, "QMD_FAKE_UPDATE_FAIL": "1"})
    assert_ok(failing, "post-ingest qmd update failure is nonfatal")
    if "qmd update 失败" not in failing.stdout:
        raise AssertionError(failing.stdout)

    for command in ["search", "vsearch", "query"]:
        result = run(["qmd", command, "Page0", "--json", "-n", "1"], env=fake_env)
        assert_ok(result, f"fake qmd {command}")
        json.loads(result.stdout)
    qmd_log = log.read_text(encoding="utf-8")
    for command in ["search", "vsearch", "query"]:
        if command not in qmd_log:
            raise AssertionError(qmd_log)


def test_skill_docs_cover_paths() -> None:
    ingest = INGEST_SKILL.read_text(encoding="utf-8")
    query = QUERY_SKILL.read_text(encoding="utf-8")
    lint = LINT_SKILL.read_text(encoding="utf-8")

    required = [
        (ingest, "不要用 `[[原始文件名]]`"),
        (ingest, "collection 不存在"),
        (ingest, "唯一必做 qmd 维护动作"),
        (ingest, "不在 ingest 中运行 `qmd vsearch` 或 `qmd query`"),
        (ingest, "不自动执行 `qmd embed`"),
        (query, "小规模检索：index.md 模式"),
        (query, "大规模检索：qmd 模式"),
        (query, "`qmd search`"),
        (query, "`qmd vsearch`"),
        (query, "`qmd query`"),
        (query, "BM25 已经返回足够相关结果"),
        (query, "`-c` 可重复传入多个 collection"),
        (query, "`--no-rerank`"),
        (query, "`-C/--candidate-limit`"),
        (query, "可能卡在 Gathering information"),
        (query, "语义命令超时回退"),
        (lint, "矛盾主张"),
        (lint, "重要概念缺页"),
        (lint, "数据空白"),
        (lint, "[[页面名#标题]]"),
        (lint, "重名文件"),
    ]
    for text, needle in required:
        if needle not in text:
            raise AssertionError(f"Missing required doc text: {needle}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="wiki-skill-tests-") as tmpdir:
        tmp = Path(tmpdir)
        make_domain(tmp, "SmallWiki", pages=3, index_lines=20)
        make_domain(tmp, "LargeWiki", pages=205, index_lines=520)
        test_scale_decision()
        test_check_domain_custom_categories(tmp)
        test_post_ingest_qmd_cases(tmp)
        test_skill_docs_cover_paths()
    print("wiki skill smoke tests passed")


if __name__ == "__main__":
    main()
