# server.py
from mcp.server.fastmcp import FastMCP
import uvicorn
import requests
import urllib3
import json

# Disable SSL warnings (optional - you can remove this if you prefer to see warnings)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create an MCP server
mcp = FastMCP("Demo",
host="0.0.0.0",
port=3001,
timeout=60,
)

# Get the ASGI app from the MCP server
app = mcp.sse_app()

def search_web(base_url: str, query: str, query_param: str = "q", additional_params: dict = None, headers: dict = None, parser_func=None) -> list[str]:
    """
    Generic web search function
    
    Args:
        base_url: Base URL for the search engine
        query: Search query string
        query_param: Query parameter name (default: "q")
        additional_params: Additional URL parameters
        headers: HTTP headers to send with request
        parser_func: Custom function to parse the response
    
    Returns:
        List of search result titles or error message
    """
    try:
        formatted_query = "+".join(query.split(" "))
        params = {query_param: formatted_query}
        
        if additional_params:
            params.update(additional_params)
        
        # Build URL with parameters
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url = f"{base_url}?{param_string}"
        
        # Default headers to mimic a browser
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        if headers:
            default_headers.update(headers)
        
        response = requests.get(url, verify=False, headers=default_headers, timeout=10)
        
        if response.status_code == 200:
            # Use custom parser if provided
            if parser_func:
                return parser_func(response, query)
            
            # Try to parse as JSON and look for organic results
            try:
                data = response.text
                return data
                # json_data = response.json()
                
                # # # Check for organic results first
                # # if 'organic' in json_data and json_data['organic']:
                # #     organic_results = json_data['organic']
                # #     results = []
                    
                # #     for result in organic_results[:10]:  # Limit to first 10 results
                # #         if isinstance(result, dict):
                # #             # Try different common fields for title
                # #             title = result.get('title') or result.get('name') or result.get('snippet', 'No title')
                # #             results.append(title)
                    
                # #     if results:
                # #         return results
                # #     else:
                # #         return [f"Search completed for '{query}' - organic results found but no titles extracted"]
                
                # # # Fallback to other result structures
                # # elif 'results' in json_data and json_data['results']:
                # #     results = json_data['results']
                # #     return [result.get("title", "No title") for result in results[:10] if isinstance(result, dict)]
                
                # # else:
                # #     return [f"Search completed for '{query}' - no organic or results array found in response"]
                # return json_data
                    
            except json.JSONDecodeError:
                # If JSON parsing fails, return basic info about the response
                content_length = len(response.text)
                return [f"Search completed for '{query}' - received {content_length} characters of non-JSON content"]
            except KeyError as e:
                return [f"Search completed for '{query}' - missing expected key: {str(e)}"]
            except Exception as e:
                return [f"Search completed for '{query}' - error parsing response: {str(e)}"]
        else:
            return [f"Error: HTTP {response.status_code} - {response.reason}"]
            
    except requests.exceptions.Timeout:
        return [f"Error: Request timeout for query '{query}'"]
    except requests.exceptions.RequestException as e:
        return [f"Error: Request failed - {str(e)}"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def parse_duckduckgo_response(response, query):
    """Parse DuckDuckGo API response"""
    try:
        data = response.json()
        results = []
        
        # Check for organic results first
        if 'organic' in data and data['organic']:
            for result in data['organic'][:5]:
                if isinstance(result, dict):
                    title = result.get('title') or result.get('snippet', 'No title')
                    results.append(title)
        
        # DuckDuckGo has different result types as fallback
        if not results:
            if "RelatedTopics" in data and data["RelatedTopics"]:
                for topic in data["RelatedTopics"][:5]:  # Limit to first 5
                    if isinstance(topic, dict) and "Text" in topic:
                        results.append(topic["Text"][:100] + "..." if len(topic["Text"]) > 100 else topic["Text"])
            
            if "Answer" in data and data["Answer"]:
                results.insert(0, f"Answer: {data['Answer']}")
            
            if "Definition" in data and data["Definition"]:
                results.insert(0, f"Definition: {data['Definition']}")
        
        if not results:
            return [f"Search completed for '{query}' - no specific results found"]
        
        return results
        
    except Exception as e:
        return [f"Error parsing DuckDuckGo response: {str(e)}"]

# Add a Google search tool
@mcp.tool()
def google(query: str) -> list[str]:
    """
    Search Google for a query and return results
    """
    return search_web(
        base_url="https://www.google.com/search",
        query=query,
        additional_params={"brd_json": "1", "num": "50"}
    )

# Add a Bing search tool
@mcp.tool()
def bing(query: str) -> list[str]:
    """
    Search Bing for a query and return results
    """
    return search_web(
        base_url="https://www.bing.com/search",
        query=query,
        additional_params={"format": "rss", "count": "10"},
        headers={'Accept': 'application/rss+xml, application/xml, text/xml'}
    )

# Add a DuckDuckGo search tool (alternative that might work better)
@mcp.tool()
def duckduckgo(query: str) -> list[str]:
    """
    Search DuckDuckGo for a query and return results
    """
    return search_web(
        base_url="https://api.duckduckgo.com/",
        query=query,
        query_param="q",
        additional_params={"format": "json", "no_redirect": "1", "no_html": "1", "skip_disambig": "1"},
        parser_func=parse_duckduckgo_response
    )

# Add a simple web search that just confirms the search was made
@mcp.tool()
def web_search_simple(query: str) -> list[str]:
    """
    Simple web search that returns a formatted response
    """
    return [f"Web search performed for: '{query}'. This is a mock search result demonstrating the search functionality."]

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Run the ASGI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
