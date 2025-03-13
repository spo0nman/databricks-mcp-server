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
   # Create and activate virtual environment
   uv venv
   
   # On Windows
   .\.venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   
   # Install dependencies
   uv pip install -e .
   
   # Install development dependencies
   uv pip install -e ".[dev]"
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

These wrapper scripts will execute the actual server scripts located in the `scripts` directory. The server will start and be ready to accept MCP protocol connections.

You can also directly run the server scripts from the scripts directory:

```bash
# Windows
.\scripts\start_mcp_server.ps1

# Linux/Mac
./scripts/start_mcp_server.sh
```

## Project Structure

```
databricks-mcp-server/
├── src/                          # Source code
│   ├── server/                   # Server implementation
│   │   ├── __init__.py
│   │   └── databricks_mcp_server.py  # Main server implementation
│   ├── api/                      # API client for Databricks services
│   │   ├── __init__.py
│   │   └── databricks_api.py     # Databricks API client
│   ├── core/                     # Core functionality and utilities
│   │   ├── __init__.py
│   │   └── utils.py              # Utility functions
│   └── cli/                      # Command-line interface
│       ├── __init__.py
│       └── mcp_cli.py            # CLI for testing the server
├── tests/                        # Test scripts (organized to mirror src/)
│   ├── server/
│   │   └── test_databricks_mcp_server.py
│   ├── api/
│   │   └── test_databricks_api.py
│   ├── core/
│   │   └── test_utils.py
│   └── cli/
│       └── test_mcp_cli.py
├── examples/                     # Example usage
│   ├── direct_usage.py           # Example of direct server usage
│   └── mcp_client_usage.py       # Example of MCP client usage
├── scripts/                      # Helper scripts
│   ├── start_mcp_server.ps1      # Main server startup script (Windows)
│   ├── start_mcp_server.sh       # Main server startup script (Linux/Mac)
│   ├── run_direct_test.ps1       # Script to run direct test (Windows)
│   ├── run_list_tools.ps1        # Script to run list tools test (Windows)
│   ├── run_mcp_client_test.ps1   # Script to run MCP client test (Windows)
│   ├── run_tests.ps1             # Script to run all tests (Windows)
│   ├── run_direct_test.sh        # Script to run direct test (Linux/Mac)
│   ├── run_list_tools.sh         # Script to run list tools test (Linux/Mac)
│   └── run_mcp_client_test.sh    # Script to run MCP client test (Linux/Mac)
├── start_mcp_server.ps1          # Wrapper script for server startup (Windows)
├── start_mcp_server.sh           # Wrapper script for server startup (Linux/Mac)
├── pyproject.toml                # Project configuration
└── README.md                     # Project documentation
```

## Development

### Code Standards

- Python code follows PEP 8 style guide with a maximum line length of 100 characters
- Use 4 spaces for indentation (no tabs)
- Use double quotes for strings
- All classes, methods, and functions should have Google-style docstrings
- Type hints are required for all code except tests

### Linting

The project uses the following linting tools:

```bash
# Run all linters
uv run pylint src/ tests/
uv run flake8 src/ tests/
uv run mypy src/
```

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
uv run pytest tests/

# Run with coverage report
uv run pytest --cov=src tests/ --cov-report=term-missing
```

A minimum code coverage of 80% is required for the project.

You can also use the provided test scripts in the scripts directory:

```bash
# Windows
.\scripts\run_direct_test.ps1      # Run direct test
.\scripts\run_list_tools.ps1       # Run list tools test
.\scripts\run_mcp_client_test.ps1  # Run MCP client test
.\scripts\run_tests.ps1            # Run all tests

# Linux/Mac
./scripts/run_direct_test.sh       # Run direct test
./scripts/run_list_tools.sh        # Run list tools test
./scripts/run_mcp_client_test.sh   # Run MCP client test
```

## Documentation

- API documentation is generated using Sphinx and can be found in the `docs/api` directory
- All code includes Google-style docstrings
- See the `examples/` directory for usage examples

## Examples

Check the `examples/` directory for usage examples. To run examples:

```bash
# Run example scripts with uv
uv run examples/direct_usage.py
uv run examples/mcp_client_usage.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Ensure your code follows the project's coding standards
2. Add tests for any new functionality
3. Update documentation as necessary
4. Verify all tests pass before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details. 