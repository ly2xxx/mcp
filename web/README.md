# Webpage Extractor MCP Server

This MCP server provides tools for extracting clean content from webpages using the Model Context Protocol.

https://github.com/modelcontextprotocol/python-sdk

## Prerequisites

- Python 3.7+
- Playwright
- BeautifulSoup4
- MCP CLI

## Installation

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
python webpage_extractor_mcp.py
```

## Claude installation

Add the MCP server to Claude:

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