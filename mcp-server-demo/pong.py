from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn

# Create an MCP server instance named "MyServer"
mcp = FastMCP("MyServer")

# Define a simple tool to illustrate server functionality
@mcp.tool()
def ping() -> str:
    """A simple ping tool returning 'pong'."""
    return "pong"

# Mount the MCP server's SSE transport on the '/sse' path using Starlette
app = Starlette(routes=[
    Mount("/sse", app=mcp.sse_app()),
])

if __name__ == "__main__":
    # Run the Starlette app with Uvicorn on localhost:3001
    uvicorn.run(app, host="127.0.0.1", port=3001)