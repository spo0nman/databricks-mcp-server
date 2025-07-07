"""
Databricks MCP Server

This module implements a standalone MCP server that provides tools for interacting
with Databricks APIs. It follows the Model Context Protocol standard, communicating
via stdio and directly connecting to Databricks when tools are invoked.
"""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional, Union, cast

from mcp.server import FastMCP
from mcp.types import TextContent
from mcp.server.stdio import stdio_server

from src.api import clusters, dbfs, jobs, notebooks, sql
from src.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabricksMCPServer:
    """Main MCP server class for Databricks integration."""
    
    def __init__(self):
        """Initialize the Databricks MCP server."""
        logger.info("Initializing Databricks MCP server")
        logger.info(f"Databricks host: {settings.DATABRICKS_HOST}")
        
        self.server = FastMCP("Databricks MCP Server")
        self._register_tools()
    
    def _register_tools(self):
        """Register all available Databricks tools."""
        
        @self.tool(
            name="list_clusters",
            description="List all Databricks clusters. Use this to see available clusters in your workspace."
        )
        async def list_clusters(params: dict = None) -> List[dict]:
            """List all clusters in the Databricks workspace."""
            try:
                result = await clusters.list_clusters()
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing clusters: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="create_cluster",
            description="Create a new Databricks cluster. Requires cluster configuration parameters like cluster_name, spark_version, and node_type_id."
        )
        async def create_cluster(params: dict) -> List[dict]:
            """Create a new cluster with the provided configuration."""
            try:
                if not params:
                    params = {}
                result = await clusters.create_cluster(params)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating cluster: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="get_cluster",
            description="Get details of a specific Databricks cluster. Requires cluster_id parameter."
        )
        async def get_cluster(params: dict) -> List[dict]:
            """Get details of a specific cluster."""
            try:
                if not params:
                    params = {}
                cluster_id = params.get("cluster_id")
                if not cluster_id:
                    return [{"type": "text", "text": "Error: cluster_id parameter is required"}]
                result = await clusters.get_cluster(cluster_id)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting cluster: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="start_cluster",
            description="Start a Databricks cluster. Requires cluster_id parameter."
        )
        async def start_cluster(params: dict) -> List[dict]:
            """Start a cluster."""
            try:
                if not params:
                    params = {}
                cluster_id = params.get("cluster_id")
                if not cluster_id:
                    return [{"type": "text", "text": "Error: cluster_id parameter is required"}]
                result = await clusters.start_cluster(cluster_id)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error starting cluster: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="terminate_cluster",
            description="Terminate a Databricks cluster. Requires cluster_id parameter."
        )
        async def terminate_cluster(params: dict) -> List[dict]:
            """Terminate a cluster."""
            try:
                if not params:
                    params = {}
                cluster_id = params.get("cluster_id")
                if not cluster_id:
                    return [{"type": "text", "text": "Error: cluster_id parameter is required"}]
                result = await clusters.terminate_cluster(cluster_id)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error terminating cluster: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="list_jobs",
            description="List all Databricks jobs. Use this to see available jobs in your workspace."
        )
        async def list_jobs(params: dict = None) -> List[dict]:
            """List all jobs in the Databricks workspace."""
            try:
                result = await jobs.list_jobs()
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing jobs: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="run_job",
            description="Run a Databricks job. Requires job_id parameter, optional notebook_params for job parameters."
        )
        async def run_job(params: dict) -> List[dict]:
            """Run a job with optional parameters."""
            try:
                if not params:
                    params = {}
                job_id = params.get("job_id")
                if not job_id:
                    return [{"type": "text", "text": "Error: job_id parameter is required"}]
                notebook_params = params.get("notebook_params", {})
                result = await jobs.run_job(job_id, notebook_params)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error running job: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="list_notebooks",
            description="List notebooks in a workspace directory. Optional path parameter (defaults to root '/' if not provided)."
        )
        async def list_notebooks(params: dict = None) -> List[dict]:
            """List notebooks in a workspace directory."""
            try:
                if not params:
                    params = {}
                path = params.get("path", "/")
                result = await notebooks.list_notebooks(path)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing notebooks: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="export_notebook",
            description="Export a notebook from the workspace. Requires path parameter, optional format parameter (JUPYTER, DBC, SOURCE, HTML)."
        )
        async def export_notebook(params: dict) -> List[dict]:
            """Export a notebook from the workspace."""
            try:
                if not params:
                    params = {}
                path = params.get("path")
                if not path:
                    return [{"type": "text", "text": "Error: path parameter is required"}]
                format_type = params.get("format", "JUPYTER")
                result = await notebooks.export_notebook(path, format_type)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error exporting notebook: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="list_files",
            description="List files and directories in DBFS. Optional dbfs_path parameter (defaults to root '/' if not provided)."
        )
        async def list_files(params: dict = None) -> List[dict]:
            """List files and directories in DBFS."""
            try:
                if not params:
                    params = {}
                dbfs_path = params.get("dbfs_path", "/")
                result = await dbfs.list_files(dbfs_path)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing files: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

        @self.tool(
            name="execute_sql",
            description="Execute a SQL statement. Requires statement and warehouse_id parameters, optional catalog and schema parameters."
        )
        async def execute_sql(params: dict) -> List[dict]:
            """Execute a SQL statement."""
            try:
                if not params:
                    params = {}
                statement = params.get("statement")
                warehouse_id = params.get("warehouse_id")
                
                if not statement:
                    return [{"type": "text", "text": "Error: statement parameter is required"}]
                if not warehouse_id:
                    return [{"type": "text", "text": "Error: warehouse_id parameter is required"}]
                
                catalog = params.get("catalog")
                schema = params.get("schema")
                result = await sql.execute_sql(statement, warehouse_id, catalog, schema)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error executing SQL: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

    @property
    def tool(self):
        """Get the tool decorator from the FastMCP server."""
        return self.server.tool

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting Databricks MCP server")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point for the Databricks MCP server."""
    try:
        server = DatabricksMCPServer()
        await server.run()
    except Exception as e:
        logger.error(f"Error in Databricks MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 