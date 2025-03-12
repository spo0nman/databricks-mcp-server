# Azure Databricks Management Control Platform (MCP)

A server platform that provides a unified interface to manage and control Azure Databricks resources through REST API endpoints.

## Features

- **Cluster Management**: Create, terminate, and list clusters
- **Job Management**: Create, run, and list jobs
- **Notebook Operations**: Import, export, and list notebooks
- **Databricks File System (DBFS)**: Upload, list, and delete files
- **SQL Statement Execution**: Execute SQL statements
- **Unity Catalog Management**: Manage catalogs, schemas, tables, and track data lineage
- **Delta Live Tables Pipelines**: Create, manage, and execute pipelines
- **Databricks SQL Queries**: Manage and execute SQL queries
- **Model Serving Endpoints**: Create, manage, and query model serving endpoints

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/databricks-mcp-server.git
cd databricks-mcp-server
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env file with your Databricks credentials
```

## Usage

1. Start the server:
```bash
python -m src.server.app
```

2. Access the API at `http://localhost:8000`

3. Connect using your client of choice:
   - Claude Desktop App
   - Cline
   - Cursor
   - Windsurf

## Development

### Running Tests
```bash
pytest
```

### Project Structure
```
databricks-mcp-server/
├── src/                  # Source code
│   ├── api/              # Databricks API integrations
│   ├── core/             # Core functionality
│   ├── server/           # Server implementation
├── tests/                # Test suite
```

## License

MIT 