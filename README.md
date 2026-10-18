# x4-mcpgen

[![CI](https://github.com/dhe-cruzer69/x4-mcpgen/actions/workflows/ci.yml/badge.svg)](https://github.com/dhe-cruzer69/x4-mcpgen/actions)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Generate production-oriented MCP server scaffolds — secure by default.**

Part of the X4 ecosystem: `x4-skills → x4-mcpgen → x4-sec → x4-runtime → x4-obs`

## 30-second demo

```bash
pip install -e ".[dev]"
x4-mcpgen init weather --tools 2
cd weather
pip install -e ".[dev]"
pytest -q
x4-mcpgen validate .
x4-mcpgen test .
```

## Why not another template?

Most MCP starters ship with broad permissions and no tests. **x4-mcpgen** produces:

- Explicit tool allow-lists (no `"*"`)
- Unit tests for every generated tool
- `SECURITY.md`, Apache-2.0, CI workflow
- `mcp.json` with stdio transport only by default
- Dockerfile with non-root user
- Ready for `x4-sec scan`

## CLI

```bash
x4-mcpgen init <name> [--tools N] [--out DIR]
x4-mcpgen validate [PATH]
x4-mcpgen test [PATH]
x4-mcpgen package [PATH]
x4-mcpgen doctor
```

## Generated layout

```text
my-mcp/
├── src/<pkg>/
│   ├── server.py
│   └── tools/
├── tests/
├── schemas/
├── Dockerfile
├── mcp.json
├── pyproject.toml
├── README.md
├── SECURITY.md
├── LICENSE
└── .github/workflows/ci.yml
```


## Architecture — Mermaid scope map

```mermaid
flowchart TD
    SPEC[Tool Definitions] --> VALID[Validate Configuration]
    VALID --> GEN[Generate MCP Project]
    GEN --> SRC[Server and Tool Modules]
    GEN --> TEST[Generated Tests]
    GEN --> POLICY[Allow-list and stdio-first Config]
    GEN --> DOCS[Security Docs and License]
    GEN --> CI[CI and Container Files]
    SRC --> CHECK[Validate and Test Generated Project]
    TEST --> CHECK
    POLICY --> CHECK
    DOCS --> CHECK
    CI --> CHECK
```

## License

Apache-2.0

## APEX Architecture Map

> Status: architecture documentation; implementation and deployment claims require independent verification.

```mermaid
flowchart LR
  Source[Canonical tool contract] --> Normalize[Normalize names and types]
  Normalize --> Validate[Validate schema constraints]
  Validate -->|invalid| Diagnostics[Actionable schema errors]
  Validate -->|valid| Generate[Generate protocol schema artifacts]
  Generate --> Determinism{Repeat generation identical?}
  Determinism -->|no| Fail[Fail determinism test]
  Determinism -->|yes| Fixtures[Update or compare golden fixtures]
  Fixtures --> Consumer[Compile / validate sample consumer]
  Consumer --> Compat{Breaking change detected?}
  Compat -->|yes| Major[Require explicit version bump]
  Compat -->|no| Package[Package generated artifacts]
  Package --> Provenance[Record generator and input version]
```
**Evidence note:** Deterministic output, compatibility checks, and consumer validation are proposed quality gates; verify they exist before claiming code generation is production-safe.

