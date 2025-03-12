"""
MCP server implementation for Databricks.
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union

from mcp import (
    MCPServer,
    Resource,
    ResourceRequest,
    Tool,
    ToolCall,
    ToolCallResult,
    ToolDefinition,
)

from src.api import clusters, dbfs, jobs, notebooks, sql
from src.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)


class DatabricksMCPServer(MCPServer):
    """MCP server for Databricks."""

    def __init__(self):
        """Initialize the server."""
        super().__init__(
            name="databricks-mcp",
            display_name="Databricks Management Control Platform",
            description="A server for managing Azure Databricks resources",
            version="0.1.0",
        )
        
        # Register tools
        self._register_tools()
        
        logger.info("Databricks MCP server initialized")
    
    def _register_tools(self):
        """Register all tools with the server."""
        # Cluster management tools
        self.register_tool(
            ToolDefinition(
                name="list_clusters",
                description="List all Databricks clusters",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "clusters": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "cluster_id": {"type": "string"},
                                    "cluster_name": {"type": "string"},
                                    "state": {"type": "string"},
                                },
                            },
                        }
                    },
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="create_cluster",
                description="Create a new Databricks cluster",
                parameters={
                    "type": "object",
                    "properties": {
                        "cluster_name": {"type": "string"},
                        "spark_version": {"type": "string"},
                        "node_type_id": {"type": "string"},
                        "num_workers": {"type": "integer"},
                        "autotermination_minutes": {"type": "integer"},
                        "spark_conf": {"type": "object"},
                        "azure_attributes": {"type": "object"},
                    },
                    "required": ["cluster_name", "spark_version", "node_type_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                    },
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="terminate_cluster",
                description="Terminate a Databricks cluster",
                parameters={
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                    },
                    "required": ["cluster_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {},
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="get_cluster",
                description="Get information about a specific Databricks cluster",
                parameters={
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                    },
                    "required": ["cluster_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                        "cluster_name": {"type": "string"},
                        "state": {"type": "string"},
                    },
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="start_cluster",
                description="Start a terminated Databricks cluster",
                parameters={
                    "type": "object",
                    "properties": {
                        "cluster_id": {"type": "string"},
                    },
                    "required": ["cluster_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {},
                },
            )
        )
        
        # Job management tools
        self.register_tool(
            ToolDefinition(
                name="list_jobs",
                description="List all Databricks jobs",
                parameters={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "jobs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "job_id": {"type": "integer"},
                                    "settings": {"type": "object"},
                                },
                            },
                        }
                    },
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="run_job",
                description="Run a Databricks job",
                parameters={
                    "type": "object",
                    "properties": {
                        "job_id": {"type": "integer"},
                        "notebook_params": {"type": "object"},
                    },
                    "required": ["job_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "run_id": {"type": "integer"},
                    },
                },
            )
        )
        
        # Notebook operations tools
        self.register_tool(
            ToolDefinition(
                name="list_notebooks",
                description="List notebooks in a workspace directory",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                    },
                    "required": ["path"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "objects": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "object_type": {"type": "string"},
                                    "language": {"type": "string"},
                                },
                            },
                        }
                    },
                },
            )
        )
        
        self.register_tool(
            ToolDefinition(
                name="export_notebook",
                description="Export a notebook from the workspace",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "format": {"type": "string", "enum": ["SOURCE", "HTML", "JUPYTER", "DBC"]},
                    },
                    "required": ["path"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "decoded_content": {"type": "string"},
                    },
                },
            )
        )
        
        # DBFS tools
        self.register_tool(
            ToolDefinition(
                name="list_files",
                description="List files and directories in a DBFS path",
                parameters={
                    "type": "object",
                    "properties": {
                        "dbfs_path": {"type": "string"},
                    },
                    "required": ["dbfs_path"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "is_dir": {"type": "boolean"},
                                    "file_size": {"type": "integer"},
                                },
                            },
                        }
                    },
                },
            )
        )
        
        # SQL tools
        self.register_tool(
            ToolDefinition(
                name="execute_sql",
                description="Execute a SQL statement",
                parameters={
                    "type": "object",
                    "properties": {
                        "statement": {"type": "string"},
                        "warehouse_id": {"type": "string"},
                        "catalog": {"type": "string"},
                        "schema": {"type": "string"},
                    },
                    "required": ["statement", "warehouse_id"],
                },
                return_value={
                    "type": "object",
                    "properties": {
                        "statement_id": {"type": "string"},
                        "status": {"type": "object"},
                        "result": {"type": "object"},
                    },
                },
            )
        )
    
    async def handle_tool_call(self, tool_call: ToolCall) -> ToolCallResult:
        """
        Handle a tool call.
        
        Args:
            tool_call: The tool call to handle
            
        Returns:
            The result of the tool call
        """
        logger.info(f"Handling tool call: {tool_call.name}")
        
        try:
            # Parse parameters
            params = tool_call.parameters or {}
            
            # Dispatch to the appropriate handler
            if tool_call.name == "list_clusters":
                result = await self._handle_list_clusters()
            elif tool_call.name == "create_cluster":
                result = await self._handle_create_cluster(params)
            elif tool_call.name == "terminate_cluster":
                result = await self._handle_terminate_cluster(params)
            elif tool_call.name == "get_cluster":
                result = await self._handle_get_cluster(params)
            elif tool_call.name == "start_cluster":
                result = await self._handle_start_cluster(params)
            elif tool_call.name == "list_jobs":
                result = await self._handle_list_jobs()
            elif tool_call.name == "run_job":
                result = await self._handle_run_job(params)
            elif tool_call.name == "list_notebooks":
                result = await self._handle_list_notebooks(params)
            elif tool_call.name == "export_notebook":
                result = await self._handle_export_notebook(params)
            elif tool_call.name == "list_files":
                result = await self._handle_list_files(params)
            elif tool_call.name == "execute_sql":
                result = await self._handle_execute_sql(params)
            else:
                raise ValueError(f"Unknown tool: {tool_call.name}")
            
            return ToolCallResult(
                id=tool_call.id,
                name=tool_call.name,
                result=result,
            )
            
        except Exception as e:
            logger.error(f"Error handling tool call: {str(e)}", exc_info=True)
            return ToolCallResult(
                id=tool_call.id,
                name=tool_call.name,
                error=str(e),
            )
    
    async def _handle_list_clusters(self) -> Dict[str, Any]:
        """Handle list_clusters tool call."""
        response = await clusters.list_clusters()
        return response
    
    async def _handle_create_cluster(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_cluster tool call."""
        response = await clusters.create_cluster(params)
        return response
    
    async def _handle_terminate_cluster(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle terminate_cluster tool call."""
        cluster_id = params.get("cluster_id")
        if not cluster_id:
            raise ValueError("cluster_id is required")
        
        response = await clusters.terminate_cluster(cluster_id)
        return response
    
    async def _handle_get_cluster(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_cluster tool call."""
        cluster_id = params.get("cluster_id")
        if not cluster_id:
            raise ValueError("cluster_id is required")
        
        response = await clusters.get_cluster(cluster_id)
        return response
    
    async def _handle_start_cluster(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle start_cluster tool call."""
        cluster_id = params.get("cluster_id")
        if not cluster_id:
            raise ValueError("cluster_id is required")
        
        response = await clusters.start_cluster(cluster_id)
        return response
    
    async def _handle_list_jobs(self) -> Dict[str, Any]:
        """Handle list_jobs tool call."""
        response = await jobs.list_jobs()
        return response
    
    async def _handle_run_job(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle run_job tool call."""
        job_id = params.get("job_id")
        if not job_id:
            raise ValueError("job_id is required")
        
        notebook_params = params.get("notebook_params")
        
        response = await jobs.run_job(job_id, notebook_params)
        return response
    
    async def _handle_list_notebooks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_notebooks tool call."""
        path = params.get("path")
        if not path:
            raise ValueError("path is required")
        
        response = await notebooks.list_notebooks(path)
        return response
    
    async def _handle_export_notebook(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle export_notebook tool call."""
        path = params.get("path")
        if not path:
            raise ValueError("path is required")
        
        format = params.get("format", "SOURCE")
        
        response = await notebooks.export_notebook(path, format)
        return response
    
    async def _handle_list_files(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_files tool call."""
        dbfs_path = params.get("dbfs_path")
        if not dbfs_path:
            raise ValueError("dbfs_path is required")
        
        response = await dbfs.list_files(dbfs_path)
        return response
    
    async def _handle_execute_sql(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle execute_sql tool call."""
        statement = params.get("statement")
        if not statement:
            raise ValueError("statement is required")
        
        warehouse_id = params.get("warehouse_id")
        if not warehouse_id:
            raise ValueError("warehouse_id is required")
        
        catalog = params.get("catalog")
        schema = params.get("schema")
        
        response = await sql.execute_statement(
            statement=statement,
            warehouse_id=warehouse_id,
            catalog=catalog,
            schema=schema,
        )
        return response


async def start_mcp_server():
    """Start the MCP server."""
    server = DatabricksMCPServer()
    await server.start()
    
    # Keep the server running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down MCP server")
        await server.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_mcp_server()) 