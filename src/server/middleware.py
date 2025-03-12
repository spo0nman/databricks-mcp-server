"""
Middleware for the Databricks MCP server.
"""

import logging
import time
from typing import Callable

from fastapi import Request

# Configure logging
logger = logging.getLogger(__name__)


async def log_request(request: Request):
    """
    Log details about the incoming request.
    
    Args:
        request: The FastAPI request object
    """
    # Get request information
    method = request.method
    url = str(request.url)
    client = request.client.host if request.client else "unknown"
    
    # Log request start
    request.state.start_time = time.time()
    logger.info(f"Request started: {method} {url} from {client}")
    
    # The function doesn't return anything, it just logs the request


def create_timing_middleware() -> Callable:
    """
    Create middleware to log request timing.
    
    Returns:
        Middleware callable
    """
    async def timing_middleware(request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = str(duration)
        
        # Log timing
        method = request.method
        url = str(request.url).split("?")[0]  # Remove query params for cleaner logs
        status_code = response.status_code
        logger.info(f"{method} {url} {status_code} - {duration:.4f}s")
        
        return response
    
    return timing_middleware 