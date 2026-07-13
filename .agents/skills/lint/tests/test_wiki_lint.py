import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "wiki_lint.py"
spec = importlib.util.spec_from_file_location("wiki_lint", SCRIPT)
wiki_lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki_lint)


class WikiLintTests(unittest.TestCase):
    def test_markdown_parser_ignores_code_inline_and_comments(self):
        text = """---
title: T
---

Real [[Page]]
`[[Inline]]`
%% [[Comment]] %%

```text
[[Code]]
## Fake
```
"""
        doc = wiki_lint.parse_markdown(text)
        self.assertEqual([link.target for link in doc.wiki_links], ["Page"])
        self.assertEqual([heading.text for heading in doc.headings], [])

    def test_index_normalization_merges_duplicate_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            domain = root / "AI"
            (domain / "wiki" / "entities").mkdir(parents=True)
            (domain / "wiki" / "concepts").mkdir(parents=True)
            (domain / "domain.md").write_text(
                """---
title: AI
---

## 分类体系

- `entities/` — entities
- `concepts/` — concepts
""",
                encoding="utf-8",
            )
            (domain / "wiki" / "entities" / "Claude.md").write_text(
                "---\ntitle: Claude\n---\n", encoding="utf-8"
            )
            (domain / "wiki" / "concepts" / "RAG.md").write_text(
                "---\ntitle: RAG\n---\n", encoding="utf-8"
            )
            (domain / "wiki" / "index.md").write_text(
                """---
title: AI Index
---

# AI Index

## Entities

- [[Claude]] — model

## concepts

_（暂无）_

## entities

_（暂无）_
""",
                encoding="utf-8",
            )

            report = wiki_lint.lint_repo(root, fix=True)
            content = (domain / "wiki" / "index.md").read_text(encoding="utf-8")
            self.assertEqual(content.count("## entities"), 1)
            self.assertNotIn("## Entities", content)
            self.assertIn("- [[Claude]] — model", content)
            self.assertIn("- [[RAG]] — 待补充", content)
            self.assertGreaterEqual(report.fixed_count, 1)

    def test_query_archive_refresh_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            domain = root / "Rust"
            (domain / "wiki" / "concepts").mkdir(parents=True)
            (domain / "domain.md").write_text(
                """---
title: Rust
---

## 分类体系

- `concepts/` — concepts
""",
                encoding="utf-8",
            )
            (domain / "wiki" / "index.md").write_text(
                "# Rust Index\n\n## concepts\n\n- [[Base]] — base\n- [[Archive]] — archive\n",
                encoding="utf-8",
            )
            (domain / "wiki" / "concepts" / "Base.md").write_text(
                "---\ntitle: Base\ndate: 2026-07-13\ntags: []\nsource_count: 1\n---\n",
                encoding="utf-8",
            )
            (domain / "wiki" / "concepts" / "Archive.md").write_text(
                """---
title: Archive
date: 2026-07-12
tags: []
source_count: 0
type: query_archive
---

# Archive

## 基于页面

- [[Base]]

## 来源

Query 归档（2026-07-12）：test
""",
                encoding="utf-8",
            )

            report = wiki_lint.lint_repo(root, fix=False)
            self.assertTrue(
                any("Archive" in issue.message and "Base" in issue.message for issue in report.issues)
            )

    def test_qmd_collection_output_parsing(self):
        output = """Collections (2):

knowledge-rust (qmd://knowledge-rust/)
  Pattern:  **/*.md
  Files:    92
  Updated:  4d ago

knowledge-ai (qmd://knowledge-ai/)
  Pattern:  **/*.md
  Files:    17
"""
        self.assertEqual(
            wiki_lint.parse_qmd_collection_list(output),
            {"knowledge-rust": 92, "knowledge-ai": 17},
        )
        self.assertEqual(
            wiki_lint.parse_qmd_collection_path(
                "Collection: knowledge-rust\n  Path:     /Users/songpengfei/knowledge/Rust/wiki\n"
            ),
            "/Users/songpengfei/knowledge/Rust/wiki",
        )


if __name__ == "__main__":
    unittest.main()
