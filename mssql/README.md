How to Use This MCP Server
This MCP server allows you to execute SQL queries on a Microsoft SQL Server through a chat interface compatible with the Model Context Protocol. Here's how to set it up and use it:
Prerequisites

Python 3.7+ installed
Microsoft SQL Server instance accessible from your server
The appropriate ODBC driver for SQL Server installed

Required Python Packages
pyodbc
starlette
uvicorn
Setup Instructions

Configure Environment Variables:
SQL_SERVER=your_sql_server_address
SQL_DATABASE=your_database_name
SQL_USERNAME=your_username
SQL_PASSWORD=your_password
SQL_DRIVER={ODBC Driver 17 for SQL Server}
PORT=8000

Run the Server:
python mssql_mcp_server.py

Send Requests:
The server exposes an endpoint at /v1/chat/completions that accepts MCP-compatible requests. You can send messages containing SQL queries, and the server will execute them and return the results.

Example Client Request
json{
  "messages": [
    {
      "role": "user",
      "content": "SELECT TOP 5 * FROM Customers"
    }
  ],
  "max_tokens": 1000
}
Features

Executes SQL queries (SELECT, INSERT, UPDATE, DELETE, etc.)
Returns SELECT results as formatted markdown tables
Handles errors gracefully
Reports affected rows for modification queries
Handles various SQL data types, including dates and binary data

Security Considerations

This implementation doesn't include authentication - you should add that for production use
Consider implementing query validation or restrictions to prevent harmful queries
Don't expose this server directly to the internet without proper security controls

Let me know if you need any clarification or want to make any modifications to the implementation!