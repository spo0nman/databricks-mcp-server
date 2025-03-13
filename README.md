# Databricks MCP Server

A Model Completion Protocol (MCP) server for Databricks that provides access to Databricks functionality via the MCP protocol. This allows LLM-powered tools to interact with Databricks clusters, jobs, notebooks, and more.

## Features

- **MCP Protocol Support**: Implements the MCP protocol to allow LLMs to interact with Databricks
- **Databricks API Integration**: Provides access to Databricks REST API functionality
- **Tool Registration**: Exposes Databricks functionality as MCP tools
- **Async Support**: Built with asyncio for efficient operation

## Available Tools

The Databricks MCP Server exposes the following tools:

- **list_clusters**: List all Databricks clusters
- **create_cluster**: Create a new Databricks cluster
- **terminate_cluster**: Terminate a Databricks cluster
- **get_cluster**: Get information about a specific Databricks cluster
- **start_cluster**: Start a terminated Databricks cluster
- **list_jobs**: List all Databricks jobs
- **run_job**: Run a Databricks job
- **list_notebooks**: List notebooks in a workspace directory
- **export_notebook**: Export a notebook from the workspace
- **list_files**: List files and directories in a DBFS path
- **execute_sql**: Execute a SQL statement

## Installation

### Prerequisites

- Python 3.10 or higher
- `uv` package manager (recommended for MCP servers)

### Setup

1. Install `uv` if you don't have it already:

   ```bash
   # MacOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows (in PowerShell)
   irm https://astral.sh/uv/install.ps1 | iex
   ```

   Restart your terminal after installation.

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/databricks-mcp-server.git
   cd databricks-mcp-server
   ```

3. Set up the project with `uv`:
   ```bash
   # Initialize the project
   uv init
   
   # Create and activate virtual environment
   uv venv
   
   # On Windows
   .\.venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   
   # Install dependencies
   uv add "mcp[cli]>=1.2.0" httpx databricks-sdk
   ```

4. Set up environment variables:
   ```bash
   # Windows
   set DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   set DATABRICKS_TOKEN=your-personal-access-token
   
   # Linux/Mac
   export DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   export DATABRICKS_TOKEN=your-personal-access-token
   ```

## Running the MCP Server

To start the MCP server, run:

```bash
# Windows
.\start_mcp_server.ps1

# Linux/Mac
./start_mcp_server.sh
```

The server will start and be ready to accept MCP protocol connections.

## Project Structure

```
databricks-mcp-server/
├── src/                          # Source code
│   ├── server/                   # Server implementation
│   │   ├── __init__.py
│   │   └── databricks_mcp_server.py  # Main server implementation
│   ├── client/                   # Client utilities
│   │   ├── __init__.py
│   │   └── databricks_client.py  # Databricks API client
│   └── cli/                      # Command-line interface
│       ├── __init__.py
│       └── mcp_cli.py            # CLI for testing the server
├── tests/                        # Test scripts
│   ├── __init__.py
│   ├── direct_test.py            # Direct test of server functionality
│   ├── mcp_client_test.py        # Test using MCP client
│   └── list_tools_test.py        # Test to list available tools
├── examples/                     # Example usage
│   ├── direct_usage.py           # Example of direct server usage
│   └── mcp_client_usage.py       # Example of MCP client usage
├── pyproject.toml                # Project configuration
├── start_mcp_server.ps1          # PowerShell script to start the server (Windows)
├── start_mcp_server.sh           # Shell script to start the server (Linux/Mac)
├── run_direct_test.ps1           # Script to run direct test
├── run_list_tools.ps1            # Script to run list tools test
├── run_mcp_client_test.ps1       # Script to run MCP client test
└── README.md                     # Project documentation
```

## Examples

Check the `examples/` directory for usage examples:

- `direct_usage.py`: Example of direct usage of the server without MCP protocol
- `mcp_client_usage.py`: Example of using MCP client to interact with the server

## Testing

To run tests, use the provided scripts:

```bash
# Windows
.\run_direct_test.ps1        # Run direct test
.\run_list_tools.ps1         # Run list tools test
.\run_mcp_client_test.ps1    # Run MCP client test

# Linux/Mac
./run_direct_test.sh         # Run direct test
./run_list_tools.sh          # Run list tools test
./run_mcp_client_test.sh     # Run MCP client test
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 