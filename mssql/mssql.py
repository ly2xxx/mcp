import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

import pyodbc
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SQL Server connection parameters - you'll need to set these as environment variables
SQL_SERVER = os.environ.get("SQL_SERVER", "localhost")
SQL_DATABASE = os.environ.get("SQL_DATABASE", "master")
SQL_USERNAME = os.environ.get("SQL_USERNAME", "sa")
SQL_PASSWORD = os.environ.get("SQL_PASSWORD", "your_password")
SQL_DRIVER = os.environ.get("SQL_DRIVER", "{ODBC Driver 17 for SQL Server}")

# MCP request schema
@dataclass
class MCPRequest:
    messages: List[Dict[str, str]]
    system: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    model: Optional[str] = None

async def parse_mcp_request(request: Request) -> MCPRequest:
    data = await request.json()
    return MCPRequest(
        messages=data.get("messages", []),
        system=data.get("system"),
        max_tokens=data.get("max_tokens"),
        temperature=data.get("temperature"),
        top_p=data.get("top_p"),
        model=data.get("model"),
    )

def get_sql_connection():
    """Establish a connection to the SQL Server"""
    connection_string = (
        f"DRIVER={SQL_DRIVER};"
        f"SERVER={SQL_SERVER};"
        f"DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};"
        f"PWD={SQL_PASSWORD}"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to SQL Server: {e}")
        raise

def execute_sql_query(query: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Execute a SQL query and return the results as a list of dictionaries"""
    try:
        conn = get_sql_connection()
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(query)
        
        # Check if this is a SELECT query with results
        if cursor.description:
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert rows to list of dictionaries
            results = []
            for row in rows:
                # Convert any non-serializable types to strings
                row_dict = {}
                for i, value in enumerate(row):
                    if isinstance(value, datetime):
                        row_dict[columns[i]] = value.isoformat()
                    elif isinstance(value, (bytes, bytearray)):
                        row_dict[columns[i]] = f"BINARY DATA ({len(value)} bytes)"
                    else:
                        row_dict[columns[i]] = value
                results.append(row_dict)
            
            return results, None
        else:
            # This was likely an INSERT, UPDATE, or DELETE
            conn.commit()
            affected_rows = cursor.rowcount
            return [], f"Query executed successfully. Affected rows: {affected_rows}"
            
    except Exception as e:
        error_message = f"Error executing SQL query: {str(e)}"
        logger.error(error_message)
        return [], error_message
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def extract_sql_query(messages: List[Dict[str, str]]) -> str:
    """
    Extract SQL query from messages.
    This function looks for the last user message and tries to find a SQL query in it.
    """
    # Get the last user message
    user_messages = [msg for msg in messages if msg.get("role") == "user"]
    if not user_messages:
        return ""
    
    last_user_message = user_messages[-1]["content"]
    
    # Try to extract anything that looks like a SQL query
    # This is a simple approach - you might want to improve this based on your needs
    # Look for content between ```sql and ``` or just plain SQL statements
    
    # First, try to find SQL code blocks
    if "```sql" in last_user_message:
        parts = last_user_message.split("```sql")
        if len(parts) > 1:
            query_part = parts[1].split("```")[0].strip()
            if query_part:
                return query_part
    
    # Then, try to find any SQL-like statements
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP"]
    for keyword in sql_keywords:
        if keyword in last_user_message.upper():
            # Very simple heuristic: return everything after finding a SQL keyword
            # In a real implementation, you might want more sophisticated parsing
            return last_user_message
    
    return last_user_message  # Return the message as is if no SQL pattern detected

async def mcp_endpoint(request: Request) -> JSONResponse:
    """MCP-compatible endpoint for SQL query execution"""
    try:
        mcp_request = await parse_mcp_request(request)
        
        # Extract SQL query from the request
        query = extract_sql_query(mcp_request.messages)
        
        if not query:
            return JSONResponse({
                "error": "No SQL query found in the messages"
            }, status_code=400)
        
        # Execute the query
        results, error = execute_sql_query(query)
        
        if error:
            # Return the error message if there was a problem
            response_content = f"Error executing SQL query: {error}"
        else:
            # Format the results as a nice table if there are results
            if results:
                # Format as markdown table
                columns = results[0].keys()
                table_header = " | ".join(columns)
                separator = " | ".join(["---" for _ in columns])
                table_rows = [" | ".join([str(row.get(col, "")) for col in columns]) for row in results]
                
                response_content = f"Query executed successfully. Results:\n\n| {table_header} |\n| {separator} |\n"
                response_content += "\n".join([f"| {row} |" for row in table_rows])
                
                # If there are too many results, add a note
                if len(results) > 50:
                    response_content += f"\n\n*Showing {len(results)} records. Total records: {len(results)}*"
            else:
                response_content = error if error else "Query executed successfully. No results returned."
        
        # Create the MCP-compatible response
        response = {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": response_content
                    },
                    "finish_reason": "stop",
                }
            ],
            "created": int(datetime.now().timestamp()),
            "model": "mssql-mcp-server"
        }
        
        return JSONResponse(response)
    
    except Exception as e:
        logger.exception("Error processing request")
        return JSONResponse({
            "error": str(e)
        }, status_code=500)

# Define Starlette routes
routes = [
    Route("/v1/chat/completions", mcp_endpoint, methods=["POST"]),
]

# Create Starlette application
app = Starlette(routes=routes)

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting MCP SQL Server on port {port}...")
    print(f"SQL Server: {SQL_SERVER}, Database: {SQL_DATABASE}")
    print("Ready to execute SQL queries!")
    
    uvicorn.run(app, host="0.0.0.0", port=port)