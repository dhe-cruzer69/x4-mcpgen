from __future__ import annotations
import argparse
from pathlib import Path
from .generator import generate_server

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="x4-mcpgen")
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("name"); i.add_argument("--tools", type=int, default=2); i.add_argument("--out", default=".")
    sub.add_parser("doctor")
    a = p.parse_args(argv)
    if a.cmd == "init":
        path = generate_server(a.name, Path(a.out), tools=a.tools)
        print(f"created {path}"); return 0
    if a.cmd == "doctor":
        for req in ("pyproject.toml", "README.md", "src"):
            print(f"  {'OK' if Path(req).exists() else 'MISSING'} {req}")
        return 0
    return 1

if __name__ == "__main__": raise SystemExit(main())
