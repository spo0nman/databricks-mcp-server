#!/usr/bin/env pwsh
# Start script for the standalone Databricks MCP server

# Activate virtual environment
. ..\databricks-mcp\Scripts\Activate.ps1

# Set environment variables if needed
# $env:DATABRICKS_HOST = "https://your-workspace.azuredatabricks.net"
# $env:DATABRICKS_TOKEN = "your-token"

# Start the server by running the module directly
Write-Host "Starting Databricks MCP server..."
python -m src.server.databricks_mcp_server 