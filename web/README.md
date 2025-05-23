# Webpage Extractor MCP Server

This MCP server provides tools for extracting clean content from webpages using the Model Context Protocol.

https://github.com/modelcontextprotocol/python-sdk

## Prerequisites

- Python 3.7+
- Playwright
- BeautifulSoup4
- MCP CLI

## Installation
0. Refresh submodule code
```bash
git submodule update --init
```
```bash
cd common && pip install -r requirements.txt
```

1. Install the required dependencies:

```bash
pip install mcp[cli] playwright bs4
```

2. Initialize Playwright:

```bash
python -m playwright install firefox
```

## Usage

Run the MCP server:

```bash
cd web
python webpage_extractor_mcp.py
```

## Claude installation

Add the MCP server to Claude STDIO mode:

```bash
mcp install .\webpage_extractor_mcp.py
```
added
```bash
    "webpage-extractor": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "D:\\code\\mcp\\web\\webpage_extractor_mcp.py"
      ]
    }
```

Or manually add to Claude SSE mode (https://developers.cloudflare.com/agents/guides/remote-mcp-server/#connect-your-remote-mcp-server-to-claude-and-other-mcp-clients-via-a-local-proxy):
```bash
{
  "mcpServers": {
    "webpage-extractor": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://127.0.0.1:3001/sse"
      ]
    }
  }
}
```
Relevant discussions:
https://www.perplexity.ai/search/claude-desktop-mcp-config-webp-IfTkMILMQp2X9F5FEtST4A 
https://www.reddit.com/r/ClaudeAI/comments/1jj80mk/how_can_i_configure_an_mcp_sse_endpoint_in_claude/?rdt=38815 


## Langflow installation
MCP Server -> SSE mode
```bash
http://host.docker.internal:3001/sse
```

## Available Tools

### extract_webpage

Extracts clean content from a webpage and returns a summary of the extraction.

Parameters:
- `url`: The URL to extract content from
- `output_dir` (optional): Directory to save files. Defaults to current directory.

Example:
```
extract_webpage("https://example.com")
```

### extract_webpage_json

Extracts clean content from a webpage and returns the full extraction results as JSON.

Parameters:
- `url`: The URL to extract content from
- `output_dir` (optional): Directory to save files. Defaults to current directory.

Example:
```
extract_webpage_json("https://example.com")
```

## Output Files

The server generates two files for each extraction:
1. A screenshot of the webpage (.png)
2. A cleaned HTML version of the webpage (.html)

These files are saved in the specified output directory with timestamps in their filenames.

## Demo - MCP tools in action
![web extract MCP demo](demo.png)
https://claude.ai/public/artifacts/aeaeb14b-20f4-4530-9bee-7da609242bfc