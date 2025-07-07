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
    filename="databricks_mcp.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DatabricksMCPServer(FastMCP):
    """An MCP server for Databricks APIs."""

    def __init__(self):
        """Initialize the Databricks MCP server."""
        super().__init__(name="databricks-mcp", 
                         version="1.0.0", 
                         instructions="Use this server to manage Databricks resources")
        logger.info("Initializing Databricks MCP server")
        logger.info(f"Databricks host: {settings.DATABRICKS_HOST}")
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all Databricks MCP tools."""
        
        # Cluster management tools
        @self.tool(
            name="list_clusters",
            description="List all Databricks clusters",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        async def list_clusters(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing clusters with params: {params}")
            try:
                result = await clusters.list_clusters()
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing clusters: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="create_cluster",
            description="Create a new Databricks cluster",
            parameters={
                "type": "object",
                "properties": {
                    "cluster_name": {
                        "type": "string",
                        "description": "Name for the new cluster"
                    },
                    "spark_version": {
                        "type": "string",
                        "description": "Spark runtime version"
                    },
                    "node_type_id": {
                        "type": "string",
                        "description": "Node type identifier"
                    },
                    "num_workers": {
                        "type": "integer",
                        "description": "Number of worker nodes",
                        "minimum": 0
                    },
                    "autotermination_minutes": {
                        "type": "integer",
                        "description": "Minutes of inactivity before auto-termination",
                        "minimum": 1
                    }
                },
                "required": ["cluster_name", "spark_version", "node_type_id"]
            }
        )
        async def create_cluster(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Creating cluster with params: {params}")
            try:
                result = await clusters.create_cluster(params)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating cluster: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="terminate_cluster",
            description="Terminate a Databricks cluster",
            parameters={
                "type": "object",
                "properties": {
                    "cluster_id": {
                        "type": "string",
                        "description": "ID of the cluster to terminate"
                    }
                },
                "required": ["cluster_id"]
            }
        )
        async def terminate_cluster(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Terminating cluster with params: {params}")
            try:
                result = await clusters.terminate_cluster(params.get("cluster_id"))
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error terminating cluster: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_cluster",
            description="Get information about a specific Databricks cluster",
            parameters={
                "type": "object",
                "properties": {
                    "cluster_id": {
                        "type": "string",
                        "description": "ID of the cluster to retrieve information for"
                    }
                },
                "required": ["cluster_id"]
            }
        )
        async def get_cluster(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting cluster info with params: {params}")
            try:
                result = await clusters.get_cluster(params.get("cluster_id"))
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting cluster info: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="start_cluster",
            description="Start a terminated Databricks cluster",
            parameters={
                "type": "object",
                "properties": {
                    "cluster_id": {
                        "type": "string",
                        "description": "ID of the cluster to start"
                    }
                },
                "required": ["cluster_id"]
            }
        )
        async def start_cluster(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Starting cluster with params: {params}")
            try:
                result = await clusters.start_cluster(params.get("cluster_id"))
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error starting cluster: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        # Job management tools
        @self.tool(
            name="list_jobs",
            description="List all Databricks jobs",
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        async def list_jobs(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing jobs with params: {params}")
            try:
                result = await jobs.list_jobs()
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing jobs: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="run_job",
            description="Run a Databricks job",
            parameters={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "ID of the job to run"
                    },
                    "notebook_params": {
                        "type": "object",
                        "description": "Parameters to pass to the notebook",
                        "additionalProperties": {"type": "string"}
                    }
                },
                "required": ["job_id"]
            }
        )
        async def run_job(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Running job with params: {params}")
            try:
                notebook_params = params.get("notebook_params", {})
                result = await jobs.run_job(params.get("job_id"), notebook_params)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error running job: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        # Notebook management tools
        @self.tool(
            name="list_notebooks",
            description="List notebooks in a workspace directory",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Workspace path to list notebooks from (defaults to root '/')",
                        "default": "/"
                    }
                },
                "required": []
            }
        )
        async def list_notebooks(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing notebooks with params: {params}")
            try:
                # Use root path as default if no path is provided
                path = params.get("path", "/")
                result = await notebooks.list_notebooks(path)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing notebooks: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="export_notebook",
            description="Export a notebook from the workspace",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the notebook to export"
                    },
                    "format": {
                        "type": "string",
                        "description": "Export format",
                        "enum": ["SOURCE", "HTML", "JUPYTER", "DBC"],
                        "default": "SOURCE"
                    }
                },
                "required": ["path"]
            }
        )
        async def export_notebook(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Exporting notebook with params: {params}")
            try:
                format_type = params.get("format", "SOURCE")
                result = await notebooks.export_notebook(params.get("path"), format_type)
                
                # For notebooks, we might want to trim the response for readability
                content = result.get("content", "")
                if len(content) > 1000:
                    summary = f"{content[:1000]}... [content truncated, total length: {len(content)} characters]"
                    result["content"] = summary
                
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error exporting notebook: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        # DBFS tools
        @self.tool(
            name="list_files",
            description="List files and directories in a DBFS path",
            parameters={
                "type": "object",
                "properties": {
                    "dbfs_path": {
                        "type": "string",
                        "description": "DBFS path to list files from (defaults to root '/')",
                        "default": "/"
                    }
                },
                "required": []
            }
        )
        async def list_files(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing files with params: {params}")
            try:
                # Use root path as default if no dbfs_path is provided
                dbfs_path = params.get("dbfs_path", "/")
                result = await dbfs.list_files(dbfs_path)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing files: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]
        
        # SQL tools
        @self.tool(
            name="execute_sql",
            description="Execute a SQL statement",
            parameters={
                "type": "object",
                "properties": {
                    "statement": {
                        "type": "string",
                        "description": "SQL statement to execute"
                    },
                    "warehouse_id": {
                        "type": "string",
                        "description": "ID of the SQL warehouse to use"
                    },
                    "catalog": {
                        "type": "string",
                        "description": "Catalog to use (optional)"
                    },
                    "schema": {
                        "type": "string",
                        "description": "Schema to use (optional)"
                    }
                },
                "required": ["statement", "warehouse_id"]
            }
        )
        async def execute_sql(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Executing SQL with params: {params}")
            try:
                statement = params.get("statement")
                warehouse_id = params.get("warehouse_id")
                catalog = params.get("catalog")
                schema = params.get("schema")
                
                result = await sql.execute_sql(statement, warehouse_id, catalog, schema)
                return [{"type": "text", "text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error executing SQL: {str(e)}")
                return [{"type": "text", "text": json.dumps({"error": str(e)})}]


async def main():
    """Main entry point for the MCP server."""
    try:
        logger.info("Starting Databricks MCP server")
        server = DatabricksMCPServer()
        
        # Use the built-in method for stdio servers
        # This is the recommended approach for MCP servers
        await server.run_stdio_async()
            
    except Exception as e:
        logger.error(f"Error in Databricks MCP server: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    # Turn off buffering in stdout
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
    
    asyncio.run(main()) 