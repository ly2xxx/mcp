# server.py
from mcp.server.fastmcp import FastMCP
import uvicorn

# Create an MCP server
mcp = FastMCP("Demo")

# Get the ASGI app from the MCP server
app = mcp.sse_app()

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Run the ASGI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)