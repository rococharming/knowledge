#!/usr/bin/env python3
"""Provision qmd's pinned local semantic models and optionally build vectors.

QMD persists model URIs in its per-machine YAML config.  In some networks the
underlying downloader blocks while fetching remote metadata even when a valid
GGUF is already cached.  This script downloads pinned files directly, verifies
their SHA-256 digests, and rewrites only the local ``models`` block to absolute
paths.  No machine-specific path is written to the Git repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


SUPPORTED_QMD_VERSION = "2.5.3"


@dataclass(frozen=True)
class ModelSpec:
    role: str
    filename: str
    url: str
    sha256: str
    size: int


MODELS = (
    ModelSpec(
        "embed",
        "Qwen3-Embedding-0.6B-Q8_0.gguf",
        "https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF/resolve/main/Qwen3-Embedding-0.6B-Q8_0.gguf",
        "06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439",
        639_150_592,
    ),
    ModelSpec(
        "generate",
        "qmd-query-expansion-1.7B-q4_k_m.gguf",
        "https://huggingface.co/tobil/qmd-query-expansion-1.7B-gguf/resolve/main/qmd-query-expansion-1.7B-q4_k_m.gguf",
        "000dfb1c06efa6a049e9f64ba921c3740e2454f62abab6fa10e77bd30bb2bcc0",
        1_282_438_912,
    ),
    ModelSpec(
        "rerank",
        "qwen3-reranker-0.6b-q8_0.gguf",
        "https://huggingface.co/ggml-org/Qwen3-Reranker-0.6B-Q8_0-GGUF/resolve/main/qwen3-reranker-0.6b-q8_0.gguf",
        "22c9979ce4fbcdc5acdc310c6641c32797eff1aa980b8f7a2db8a8ea23429a48",
        639_153_184,
    ),
)


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str


def cache_dir() -> Path:
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")).expanduser()
    return base / "qmd" / "models"


def config_dir() -> Path:
    if os.environ.get("QMD_CONFIG_DIR"):
        return Path(os.environ["QMD_CONFIG_DIR"]).expanduser()
    if os.environ.get("XDG_CONFIG_HOME"):
        return Path(os.environ["XDG_CONFIG_HOME"]).expanduser() / "qmd"
    return Path.home() / ".config" / "qmd"


def config_path(index: str = "index") -> Path:
    return config_dir() / f"{index}.yml"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def model_is_valid(path: Path, spec: ModelSpec) -> bool:
    return path.is_file() and path.stat().st_size == spec.size and sha256_file(path) == spec.sha256


def download_model(spec: ModelSpec, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{spec.filename}.", suffix=".part", dir=destination.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        request = urllib.request.Request(spec.url, headers={"User-Agent": "llm-wiki-qmd-bootstrap/1"})
        with urllib.request.urlopen(request) as response, temporary.open("wb") as output:
            while block := response.read(1024 * 1024):
                output.write(block)
        if not model_is_valid(temporary, spec):
            raise RuntimeError(f"模型校验失败：{spec.filename}")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def expected_models(model_dir: Optional[Path] = None) -> dict[str, str]:
    root = (model_dir or cache_dir()).expanduser().resolve()
    return {spec.role: str(root / spec.filename) for spec in MODELS}


def parse_models_block(text: str) -> dict[str, str]:
    match = re.search(r"(?ms)^models:\s*\n((?:^[ \t]+.*(?:\n|$))*)", text)
    if not match:
        return {}
    models: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^\s+(embed|generate|rerank):\s*(.+?)\s*$", line)
        if item:
            models[item.group(1)] = item.group(2).strip().strip('"\'')
    return models


def rewrite_models_block(text: str, models: dict[str, str]) -> str:
    block = "models:\n" + "".join(f"  {role}: {json.dumps(models[role], ensure_ascii=False)}\n" for role in ("embed", "generate", "rerank"))
    pattern = r"(?ms)^models:\s*\n(?:^[ \t]+.*(?:\n|$))*"
    if re.search(pattern, text):
        return re.sub(pattern, block, text, count=1)
    separator = "" if not text or text.endswith("\n") else "\n"
    return f"{text}{separator}{block}"


def qmd_version() -> Optional[str]:
    try:
        completed = subprocess.run(["qmd", "--version"], check=False, text=True, capture_output=True)
    except FileNotFoundError:
        return None
    match = re.search(r"\b(\d+\.\d+\.\d+)\b", completed.stdout + completed.stderr)
    return match.group(1) if completed.returncode == 0 and match else None


def provision(index: str, apply: bool, run_embed: bool = False, run_doctor: bool = False) -> dict:
    findings: list[Finding] = []
    changed = False
    embedded = False
    version = qmd_version()
    if version is None:
        findings.append(Finding("error", "qmd_missing", "未找到 qmd；先安装 @tobilu/qmd@2.5.3"))
        return build_result(findings, changed, embedded)
    if version != SUPPORTED_QMD_VERSION:
        findings.append(
            Finding("error", "qmd_version", f"qmd 版本为 {version}；本知识库锁定并验证的是 {SUPPORTED_QMD_VERSION}")
        )
        return build_result(findings, changed, embedded)

    target_config = config_path(index)
    if not target_config.is_file():
        findings.append(Finding("error", "config_missing", f"缺少 {target_config}；先运行 qmd_sync.py --apply"))
        return build_result(findings, changed, embedded)

    model_dir = cache_dir()
    expected = expected_models(model_dir)
    for spec in MODELS:
        destination = model_dir / spec.filename
        if model_is_valid(destination, spec):
            continue
        if not apply:
            findings.append(Finding("warning", "model_missing", f"模型缺失或校验失败：{destination}"))
            continue
        try:
            download_model(spec, destination)
        except Exception as error:  # noqa: BLE001 - surface a concise bootstrap failure
            findings.append(Finding("error", "download_failed", f"{spec.filename} 下载失败：{error}"))
            continue
        changed = True
        findings.append(Finding("fixed", "model_downloaded", f"已下载并校验：{spec.filename}"))

    if any(f.level == "error" for f in findings):
        return build_result(findings, changed, embedded)

    text = target_config.read_text(encoding="utf-8")
    actual = parse_models_block(text)
    config_changed = actual != expected
    if config_changed:
        if apply:
            target_config.write_text(rewrite_models_block(text, expected), encoding="utf-8")
            changed = True
            findings.append(Finding("fixed", "config_localized", f"已将模型配置指向本机缓存：{target_config}"))
        else:
            findings.append(Finding("warning", "remote_model_uri", "qmd 模型配置尚未指向已校验的本地文件"))

    if run_embed and apply:
        command = ["qmd", "embed"]
        if config_changed:
            command.append("-f")
        completed = subprocess.run(command, check=False, text=True, capture_output=True)
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or f"退出码 {completed.returncode}"
            findings.append(Finding("error", "embed_failed", f"qmd embed 失败：{detail.splitlines()[0]}"))
        else:
            embedded = True
            findings.append(Finding("fixed", "embedded", "向量索引已生成或增量更新"))

    if run_doctor and apply and not any(f.level == "error" for f in findings):
        completed = subprocess.run(["qmd", "doctor"], check=False, text=True, capture_output=True)
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip() or f"退出码 {completed.returncode}"
            findings.append(Finding("error", "doctor_failed", f"qmd doctor 失败：{detail.splitlines()[0]}"))
        else:
            findings.append(Finding("fixed", "doctor_ok", "qmd 本地模型实际推理检查通过"))

    return build_result(findings, changed, embedded)


def build_result(findings: list[Finding], changed: bool, embedded: bool) -> dict:
    has_error = any(f.level == "error" for f in findings)
    needs_action = any(f.level == "warning" for f in findings)
    status = "error" if has_error else "needs_setup" if needs_action else "changed" if changed else "ok"
    return {
        "status": status,
        "exit_code": 2 if has_error else 1 if needs_action else 0,
        "changed": changed,
        "embedded": embedded,
        "findings": [asdict(finding) for finding in findings],
    }


def print_human(result: dict) -> None:
    print(f"qmd-semantic: {result['status']}")
    if not result["findings"]:
        print("- 模型文件、校验值和本机配置均正常")
    for finding in result["findings"]:
        print(f"- {finding['level'].upper()}: {finding['message']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Provision pinned local qmd semantic models")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="Read-only model and local-config check")
    modes.add_argument("--apply", action="store_true", help="Download, verify, and configure pinned models")
    parser.add_argument("--embed", action="store_true", help="With --apply, build or incrementally refresh vectors")
    parser.add_argument("--doctor", action="store_true", help="With --apply, run qmd's actual inference health check")
    parser.add_argument("--index", default="index", help="Named qmd index (default: index)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args()
    if (args.embed or args.doctor) and not args.apply:
        parser.error("--embed/--doctor requires --apply")
    result = provision(args.index, args.apply, args.embed, args.doctor)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print_human(result)
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
