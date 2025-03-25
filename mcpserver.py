from mcp.server.fastmcp import FastMCP

# Create an MCP server
server = FastMCP("my-python-mcp")

# Add capabilities like tools
@server.tool()
def example_tool(arg1: str) -> str:
    """Example tool description"""
    return f"Processed: {arg1}"

# Add dynamic resources
@server.resource("example://{param}")
def get_example(param: str) -> str:
    """Example resource"""
    return f"Resource data for {param}"

# Run the server
if __name__ == "__main__":
    server.run()