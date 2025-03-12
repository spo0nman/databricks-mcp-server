"""
Router modules for the Databricks MCP server.
"""

from src.server.routers.clusters import router as clusters_router
from src.server.routers.jobs import router as jobs_router
from src.server.routers.notebooks import router as notebooks_router
from src.server.routers.dbfs import router as dbfs_router
from src.server.routers.sql import router as sql_router

__all__ = [
    "clusters_router",
    "jobs_router",
    "notebooks_router",
    "dbfs_router",
    "sql_router",
] 