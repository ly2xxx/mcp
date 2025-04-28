from mcp.server.fastmcp import FastMCP
import uvicorn

# Create an MCP server instance named "MyServer"
mcp = FastMCP("MyServer")

# Define a simple tool to illustrate server functionality
@mcp.tool()
def ping() -> str:
    """A simple ping tool returning 'pong'."""
    return "pong"

# Get the ASGI app from the MCP server
app = mcp.asgi_app()

if __name__ == "__main__":
    # Run the ASGI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)

