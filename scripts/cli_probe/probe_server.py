"""One-tool MCP server for testing tool access from `claude -p`.

The tool returns the value of PROBE_VALUE, set per run by the test, so the
model can report it only by calling the tool.
"""
import os

from mcp.server.mcpserver import MCPServer

server = MCPServer("probe")


@server.tool()
def get_probe_value() -> str:
    """Return the probe value for this run."""
    return os.environ.get("PROBE_VALUE", "unset")


if __name__ == "__main__":
    server.run("stdio")
