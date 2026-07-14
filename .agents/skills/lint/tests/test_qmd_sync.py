import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "init-domain" / "scripts" / "qmd_sync.py"
SPEC = importlib.util.spec_from_file_location("qmd_sync", SCRIPT)
qmd_sync = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = qmd_sync
SPEC.loader.exec_module(qmd_sync)


class FakeRunner:
    def __init__(self, collection_list="", show_output=""):
        self.collection_list = collection_list
        self.show_output = show_output
        self.calls = []

    def __call__(self, args, cwd):
        self.calls.append(args)
        if args[:3] == ["qmd", "collection", "list"]:
            return qmd_sync.CommandResult(0, self.collection_list)
        if args[:3] == ["qmd", "collection", "show"]:
            return qmd_sync.CommandResult(0, self.show_output)
        return qmd_sync.CommandResult(0, "ok")


class QmdSyncTests(unittest.TestCase):
    def make_repo(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "Rust" / "wiki").mkdir(parents=True)
        (root / "Rust" / "domain.md").write_text(
            """# Rust 领域规则

## 领域概述

Rust 编程语言学习与实践知识库。

## qmd 配置

- collection 名称：`knowledge-rust`
- collection root：`Rust/wiki`
""",
            encoding="utf-8",
        )
        return temp, root

    def test_check_reports_missing_without_mutation(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner()

        result = qmd_sync.synchronize(root, "check", runner=runner)

        self.assertEqual(result["status"], "needs_sync")
        self.assertEqual(result["exit_code"], 1)
        self.assertEqual([call[:3] for call in runner.calls], [["qmd", "collection", "list"]])

    def test_apply_registers_context_and_updates_once(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner()

        result = qmd_sync.synchronize(root, "apply", runner=runner)

        self.assertEqual(result["status"], "changed")
        self.assertTrue(result["updated"])
        self.assertEqual(sum(call[:3] == ["qmd", "collection", "add"] for call in runner.calls), 1)
        self.assertEqual(sum(call[:3] == ["qmd", "context", "add"] for call in runner.calls), 1)
        self.assertEqual(sum(call == ["qmd", "update"] for call in runner.calls), 1)
        self.assertFalse(any("embed" in call for call in runner.calls))

    def test_apply_is_idempotent_when_healthy(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner(
            "knowledge-rust (qmd://knowledge-rust/)\n  Files: 0\n",
            f"Collection: knowledge-rust\n  Path: {root / 'Rust' / 'wiki'}\n  Contexts: 1\n",
        )

        result = qmd_sync.synchronize(root, "apply", runner=runner)

        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["updated"])
        self.assertFalse(any(call == ["qmd", "update"] for call in runner.calls))

    def test_refresh_updates_healthy_config_once(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner(
            "knowledge-rust (qmd://knowledge-rust/)\n  Files: 0\n",
            f"Collection: knowledge-rust\n  Path: {root / 'Rust' / 'wiki'}\n  Contexts: 1\n",
        )

        result = qmd_sync.synchronize(root, "apply", refresh=True, runner=runner)

        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["updated"])
        self.assertEqual(sum(call == ["qmd", "update"] for call in runner.calls), 1)

    def test_apply_adds_context_when_show_omits_contexts_line(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner(
            "knowledge-rust (qmd://knowledge-rust/)\n  Files: 0\n",
            f"Collection: knowledge-rust\n  Path: {root / 'Rust' / 'wiki'}\n",
        )

        result = qmd_sync.synchronize(root, "apply", runner=runner)

        self.assertEqual(result["status"], "changed")
        self.assertEqual(sum(call[:3] == ["qmd", "context", "add"] for call in runner.calls), 1)
        self.assertEqual(sum(call == ["qmd", "update"] for call in runner.calls), 1)

    def test_path_conflict_never_mutates(self):
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        runner = FakeRunner(
            "knowledge-rust (qmd://knowledge-rust/)\n  Files: 0\n",
            "Collection: knowledge-rust\n  Path: /old/knowledge/Rust/wiki\n  Contexts: 1\n",
        )

        result = qmd_sync.synchronize(root, "apply", refresh=True, runner=runner)

        self.assertEqual(result["status"], "conflict")
        self.assertEqual(result["exit_code"], 2)
        self.assertFalse(any(call == ["qmd", "update"] for call in runner.calls))
        self.assertFalse(any(call[:3] == ["qmd", "collection", "add"] for call in runner.calls))


if __name__ == "__main__":
    unittest.main()
