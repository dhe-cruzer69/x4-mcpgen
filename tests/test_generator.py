from __future__ import annotations

from pathlib import Path

from x4_mcpgen.generator import generate_server
from x4_mcpgen.validate import validate_scaffold
from x4_mcpgen.cli import main


def test_generate_and_validate(tmp_path: Path) -> None:
    root = generate_server("demo-weather", tmp_path, tools=2)
    assert (root / "mcp.json").exists()
    assert (root / "Dockerfile").exists()
    assert (root / "src" / "demo_weather" / "server.py").exists()
    assert (root / "tests" / "test_health.py").exists()
    assert validate_scaffold(root) == []


def test_no_wildcard_permissions(tmp_path: Path) -> None:
    root = generate_server("safe", tmp_path, tools=1)
    text = (root / "mcp.json").read_text()
    assert '"*"' not in text
    assert '"shell": "deny"' in text


def test_cli_init(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["init", "cli-demo", "--tools", "1"]) == 0
    assert (tmp_path / "cli-demo" / "mcp.json").exists()
