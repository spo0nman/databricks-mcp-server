"""
FastAPI server application for the Databricks MCP.
"""

import logging
import sys
from typing import Dict

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import settings
from src.core.utils import DatabricksAPIError
from src.server.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title="Databricks Management Control Platform",
        description="API server for managing Azure Databricks resources",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register API routes
    app.include_router(api_router, prefix="/api")
    
    # Add exception handlers
    @app.exception_handler(DatabricksAPIError)
    async def databricks_api_error_handler(request: Request, exc: DatabricksAPIError) -> JSONResponse:
        """Handle Databricks API errors."""
        status_code = exc.status_code if exc.status_code else 500
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "error": str(exc),
                "status_code": status_code,
                "response": exc.response,
            },
        )
    
    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        """Run on server startup."""
        logger.info("Starting Databricks MCP server")
    
    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Run on server shutdown."""
        logger.info("Shutting down Databricks MCP server")
    
    # Add root route
    @app.get("/", tags=["Root"])
    async def root() -> Dict[str, str]:
        """Root endpoint."""
        return {
            "message": "Welcome to the Databricks Management Control Platform API",
            "docs": "/docs",
        }
    
    return app


app = create_app()


def start_server():
    """Start the server."""
    uvicorn.run(
        "src.server.app:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start_server() 