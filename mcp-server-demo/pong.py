from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount, Route
import uvicorn

# Create an MCP server instance named "MyServer"
mcp = FastMCP("MyServer")

# Define a simple tool to illustrate server functionality
@mcp.tool()
def ping() -> str:
    """A simple ping tool returning 'pong'."""
    return "pong"

# Get the SSE app
sse_app = mcp.sse_app()

# Get the message handler
async def message_handler(request):
    return await mcp.handle_message(request)

# Mount the MCP server's endpoints
app = Starlette(routes=[
    Route("/sse", endpoint=sse_app),
    Route("/sse/", endpoint=sse_app),
    Route("/messages", endpoint=message_handler, methods=["POST"]),
    Route("/messages/", endpoint=message_handler, methods=["POST"]),
])

if __name__ == "__main__":
    # Run the Starlette app with Uvicorn on all interfaces
    uvicorn.run(app, host="0.0.0.0", port=3001)

