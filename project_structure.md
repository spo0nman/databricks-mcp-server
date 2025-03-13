```
databricks-mcp-server/
├── src/                             # Source code
│   ├── __init__.py                  # Makes src a package
│   ├── api/                         # Databricks API clients
│   │   ├── __init__.py              # Makes api a package
│   │   ├── clusters.py              # Cluster API
│   │   ├── dbfs.py                  # DBFS API
│   │   ├── jobs.py                  # Jobs API
│   │   ├── notebooks.py             # Notebooks API
│   │   └── sql.py                   # SQL API
│   ├── core/                        # Core functionality
│   │   ├── __init__.py              # Makes core a package
│   │   ├── config.py                # Configuration management
│   │   └── utils.py                 # Utility functions
│   ├── server/                      # Server implementation
│   │   ├── __init__.py              # Makes server a package
│   │   └── databricks_mcp_server.py # Main MCP server
│   └── cli/                         # Command-line interface
│       ├── __init__.py              # Makes cli a package 
│       └── commands.py              # CLI commands
├── tests/                           # Test directory
│   ├── __init__.py                  # Makes tests a package
│   ├── test_direct.py               # Direct server tests
│   ├── test_mcp_client.py           # MCP client tests
│   └── test_tools.py                # Individual tool tests
├── scripts/                         # Scripts directory
│   ├── start_server.ps1             # Server startup script
│   ├── run_tests.ps1                # Test runner script
│   └── run_list_tools.ps1           # Tool listing script
├── examples/                        # Example usage
│   ├── direct_usage.py              # Direct server usage
│   ├── mcp_client_usage.py          # Client example
│   └── README.md                    # Examples documentation
├── docs/                            # Documentation
│   ├── api.md                       # API documentation
│   ├── tools.md                     # Tool documentation
│   ├── setup.md                     # Setup instructions
│   └── architecture.md              # Architecture overview
├── .env.example                     # Example environment file
├── .gitignore                       # Git ignore file
├── README.md                        # Main README
├── LICENSE                          # License file
├── requirements.txt                 # Python dependencies
├── setup.py                         # Package setup file
└── pyproject.toml                   # Modern Python packaging
``` 