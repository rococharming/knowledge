import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "init-domain" / "scripts" / "qmd_semantic.py"
SPEC = importlib.util.spec_from_file_location("qmd_semantic", SCRIPT)
qmd_semantic = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = qmd_semantic
SPEC.loader.exec_module(qmd_semantic)


class QmdSemanticTests(unittest.TestCase):
    def test_rewrite_models_block_preserves_collections(self):
        original = (
            "collections:\n"
            "  notes:\n"
            "    path: /tmp/notes\n"
            "models:\n"
            "  embed: hf:old/embed.gguf\n"
            "  generate: hf:old/generate.gguf\n"
            "  rerank: hf:old/rerank.gguf\n"
        )
        expected = {
            "embed": "/tmp/models/embed.gguf",
            "generate": "/tmp/models/generate.gguf",
            "rerank": "/tmp/models/rerank.gguf",
        }
        rewritten = qmd_semantic.rewrite_models_block(original, expected)
        self.assertIn("path: /tmp/notes", rewritten)
        self.assertEqual(qmd_semantic.parse_models_block(rewritten), expected)

    def test_rewrite_models_block_appends_when_missing(self):
        expected = {
            "embed": "/tmp/embed.gguf",
            "generate": "/tmp/generate.gguf",
            "rerank": "/tmp/rerank.gguf",
        }
        rewritten = qmd_semantic.rewrite_models_block("collections: {}\n", expected)
        self.assertEqual(qmd_semantic.parse_models_block(rewritten), expected)

    def test_model_validation_checks_size_and_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.gguf"
            path.write_bytes(b"GGUF-test")
            spec = qmd_semantic.ModelSpec(
                "embed",
                path.name,
                "https://example.invalid/model.gguf",
                qmd_semantic.hashlib.sha256(b"GGUF-test").hexdigest(),
                len(b"GGUF-test"),
            )
            self.assertTrue(qmd_semantic.model_is_valid(path, spec))
            path.write_bytes(b"corrupt")
            self.assertFalse(qmd_semantic.model_is_valid(path, spec))


if __name__ == "__main__":
    unittest.main()
