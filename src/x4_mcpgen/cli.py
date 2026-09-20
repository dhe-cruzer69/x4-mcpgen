from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import __version__
from .generator import generate_server
from .validate import validate_scaffold


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="x4-mcpgen",
        description="Generate secure-by-default MCP server scaffolds",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    init = sub.add_parser("init", help="Create a new MCP server scaffold")
    init.add_argument("name", help="Server name")
    init.add_argument("--tools", type=int, default=2, help="Number of placeholder tools (1-20)")
    init.add_argument("--out", default=".", help="Output directory")

    val = sub.add_parser("validate", help="Validate an existing scaffold")
    val.add_argument("path", nargs="?", default=".")

    test_p = sub.add_parser("test", help="Run pytest in scaffold")
    test_p.add_argument("path", nargs="?", default=".")

    pkg = sub.add_parser("package", help="Build wheel/sdist if pyproject present")
    pkg.add_argument("path", nargs="?", default=".")

    sub.add_parser("doctor", help="Check local environment")

    args = p.parse_args(argv)

    if args.cmd == "init":
        path = generate_server(args.name, Path(args.out), tools=args.tools)
        print(f"created {path}")
        print("next: cd", path.name, "&& pip install -e '.[dev]' && pytest -q")
        return 0

    if args.cmd == "validate":
        root = Path(args.path)
        errs = validate_scaffold(root)
        if errs:
            for e in errs:
                print(f"FAIL {e}", file=sys.stderr)
            return 1
        print("OK scaffold valid")
        return 0

    if args.cmd == "test":
        root = Path(args.path)
        r = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=root,
            check=False,
        )
        return r.returncode

    if args.cmd == "package":
        root = Path(args.path)
        r = subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=root,
            check=False,
        )
        return r.returncode

    if args.cmd == "doctor":
        for req in ("pyproject.toml", "README.md", "src"):
            exists = Path(req).exists()
            print(f"  {'OK' if exists else 'MISSING'} {req}")
        print(f"  python {sys.version.split()[0]}")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
