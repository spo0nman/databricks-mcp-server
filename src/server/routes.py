"""
API routes for the Databricks MCP server.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.auth import validate_api_key
from src.server.middleware import log_request
from src.server.routers import (
    clusters_router,
    jobs_router,
    notebooks_router,
    dbfs_router,
    sql_router,
)

# Create main router
router = APIRouter()

# Add middleware
router.dependencies.append(Depends(log_request))

# Include sub-routers
router.include_router(
    clusters_router,
    prefix="/clusters",
    tags=["Clusters"],
    dependencies=[Depends(validate_api_key)],
)

router.include_router(
    jobs_router,
    prefix="/jobs",
    tags=["Jobs"],
    dependencies=[Depends(validate_api_key)],
)

router.include_router(
    notebooks_router,
    prefix="/notebooks",
    tags=["Notebooks"],
    dependencies=[Depends(validate_api_key)],
)

router.include_router(
    dbfs_router,
    prefix="/dbfs",
    tags=["DBFS"],
    dependencies=[Depends(validate_api_key)],
)

router.include_router(
    sql_router,
    prefix="/sql",
    tags=["SQL"],
    dependencies=[Depends(validate_api_key)],
)

# Health check endpoint (no auth required)
@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"} 