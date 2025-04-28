import os
import sys
import json
from typing import Optional
# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mcp.server.fastmcp import FastMCP
from common.webpage_extractor.webpage_extractor.extract_cleaner_webpage_sync import extract_clean_content
import uvicorn

# Initialize FastMCP server
mcp = FastMCP("webpage-extractor")

# Get the ASGI app from the MCP server
app = mcp.sse_app()

@mcp.tool()
async def extract_webpage(url: str, output_dir: Optional[str] = None) -> str:
    """
    Extract clean content from a webpage and return a summary of the extraction.
    
    Args:
        url: The URL to extract content from
        output_dir: Directory to save files. Defaults to current directory.
    
    Returns:
        A summary of the extracted content and paths to saved files.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if output_dir is None:
        output_dir = os.getcwd()
    
    try:
        result = await extract_clean_content(url, output_dir)
        
        # Format the response
        clean_data = result['clean_data']
        
        # Format main content for display
        content_summary = []
        for item in clean_data['main_content'][:5]:  # Limit to first 5 items
            content_summary.append(f"{item['type'].upper()}: {item['text'][:100]}...")
        
        # Format links for display
        links_summary = []
        for link in clean_data['links'][:5]:  # Limit to first 5 links
            links_summary.append(f"- {link['text'][:50]}: {link['url']}")
        
        response = f"""
            Webpage Extraction Results for: {url}

            Title: {clean_data['title']}
            """
            # Content Preview:
            # {"".join(f"{item}\n" for item in content_summary)}

            # Links Preview:
            # {"".join(f"{link}\n" for link in links_summary)}

            # Files saved:
            # - HTML: {result['html_path']}
            # - JSON: {result['json_path']}
            # - Text: {result['text_path']}
            # """
        return response
    
    except Exception as e:
        return f"Error extracting content from {url}: {str(e)}"

@mcp.tool()
async def extract_webpage_json(url: str, output_dir: Optional[str] = None) -> str:
    """
    Extract clean content from a webpage and return the full extraction results as JSON.
    
    Args:
        url: The URL to extract content from
        output_dir: Directory to save files. Defaults to current directory.
    
    Returns:
        JSON string containing all extracted data.
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if output_dir is None:
        output_dir = os.getcwd()
    
    try:
        result = await extract_clean_content(url, output_dir)
        
        # Convert paths to relative paths for better portability
        result['screenshot_path'] = os.path.basename(result['screenshot_path'])
        result['html_path'] = os.path.basename(result['html_path'])
        
        # Return as formatted JSON string
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
    
# if __name__ == "__main__":
#     print("Starting webpage extractor MCP server...")
#     mcp.run(transport='stdio')

if __name__ == "__main__":
    print("Starting webpage extractor MCP server...")
    # Run the ASGI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)