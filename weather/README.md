https://modelcontextprotocol.io/quickstart/server
https://github.com/jdhettema/mcp-weather-sse

# Install uv - python package management
windows -- 
'''powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
'''
MacOS/Linux --
'''
curl -LsSf https://astral.sh/uv/install.sh | sh
'''

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