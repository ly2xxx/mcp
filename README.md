"# mcp" 
https://gitmcp.io/ly2xxx/mcp

https://collabnix.com/how-to-build-and-host-your-own-mcp-servers-in-easy-steps

https://github.com/modelcontextprotocol/servers

https://smithery.ai/

https://mcp.so/

https://cursor.directory/mcp

Docker - https://huggingface.co/blog/lynn-mikami/markitdown-mcp

## MCP client
[![ MCP client](https://img.youtube.com/vi/L94WBLL0KjY/hqdefault.jpg)](https://m.youtube.com/watch?v=L94WBLL0KjY)

## MCP server
[![ MCP server](https://img.youtube.com/vi/qb95jXnCOdc/hqdefault.jpg)](https://m.youtube.com/watch?v=qb95jXnCOdc)

## MCP holistic
[![ MCP holistic](https://img.youtube.com/vi/_d0duu3dED4/hqdefault.jpg)](https://m.youtube.com/watch?v=_d0duu3dED4)

## MCP in langflow
[![ MCP langflow](https://img.youtube.com/vi/pEjsaVVPjdI/hqdefault.jpg)](https://www.youtube.com/watch?v=pEjsaVVPjdI)

## MCP self-host
[![ MCP self-host](https://img.youtube.com/vi/OUPW4DJMAsA/hqdefault.jpg)](https://www.youtube.com/watch?v=OUPW4DJMAsA)

Code in https://modelcontextprotocol.io/quickstart/server 


## Run 3rd party MCP server in SSE mode - example
```bash
git submodule add https://github.com/haris-musa/excel-mcp-server.git excel-mcp-server
```
```bash
pip install uv
```
```bash
cd excel-mcp-server
```
```bash
uv venv
```
```bash
.venv\Scripts\activate
```
```bash
uv pip install -e .
```
```bash
uv run excel-mcp-server
```
Add following configuration
```bash
{
  "mcpServers": {
    "excel": {
      "url": "http://localhost:8000/sse",
      "env": {
        "EXCEL_FILES_PATH": "/path/to/excel/files"
      }
    }
  }
}
```
