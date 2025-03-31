https://modelcontextprotocol.io/quickstart/server

# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
.venv\Scripts\activate

# Install dependencies
uv add mcp[cli] httpx

# Create our server file
new-item weather.py

# Run weather.py
uv run weather.py