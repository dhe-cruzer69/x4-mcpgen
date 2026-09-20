from __future__ import annotations

import json
from pathlib import Path


def validate_scaffold(root: Path) -> list[str]:
    """Return list of validation errors (empty = ok)."""
    errors: list[str] = []
    required = [
        "pyproject.toml",
        "README.md",
        "SECURITY.md",
        "LICENSE",
        "mcp.json",
        "Dockerfile",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"missing {rel}")

    mcp_path = root / "mcp.json"
    if mcp_path.exists():
        try:
            data = json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"mcp.json invalid JSON: {e}")
        else:
            perms = data.get("permissions") or {}
            tools = data.get("tools")
            if tools is None:
                errors.append("mcp.json: tools must be explicit list")
            elif isinstance(tools, list):
                for t in tools:
                    if t == "*" or (isinstance(t, dict) and t.get("name") == "*"):
                        errors.append("mcp.json: wildcard tool not allowed")
            if perms.get("shell") not in (None, "deny"):
                errors.append("mcp.json: shell should be deny by default")
            transports = data.get("transports") or []
            if "stdio" not in transports and transports:
                errors.append("mcp.json: prefer stdio transport for local servers")

    # no curl|bash in tree
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(x in p.parts for x in (".git", ".venv", "node_modules")):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "curl " in text and "| bash" in text:
            errors.append(f"dangerous pipe-to-shell pattern in {p.relative_to(root)}")

    return errors
