#!/usr/bin/env python3
"""
FastAPI Server Configuration
"""
import uvicorn
from src.api.api import api

def start_server():
    """Start the FastAPI server with uvicorn"""
    uvicorn.run(
        app=api,  # Direct app instance
        host="127.0.0.1",  # localhost
        port=8000,
        reload=True,        # Auto-reload on file changes
        log_level="info",
        access_log=True,
        workers=1           # Single worker for development
    )

def start_production_server():
    """Start the server in production mode"""
    uvicorn.run(
        "src.api.api:api",  # Module path for multi-worker support
        host="0.0.0.0",     # Accept external connections
        port=8000,
        reload=False,       # No auto-reload in production
        log_level="warning",
        workers=4           # Multiple workers for production
    )

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        print("🚀 Starting production server...")
        start_production_server()
    else:
        print("🔧 Starting development server...")
        start_server()