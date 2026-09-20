from x4_mcpgen.generator import generate_server

def test_gen(tmp_path):
    p = generate_server("demo", tmp_path, tools=2)
    assert (p / "mcp.json").exists()
    assert (p / "src" / "demo" / "server.py").exists()
