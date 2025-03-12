#!/usr/bin/env python
"""
Script to run the Databricks API server.
"""

import sys

from src.server.app import start_server

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0) 