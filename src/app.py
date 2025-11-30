import logging
import uvicorn
from pydantic import BaseModel, Field
from fastapi import FastAPI

from src.core.logger import configure_logger

# Configure logger once at module level
configure_logger()
logger = logging.getLogger(__name__)

class BlogApp(BaseModel):
    """
    A class for the blog application with server configuration management.
    
    This class encapsulates the uvicorn server configuration and provides
    a clean interface to start the FastAPI application.
    
    Attributes:
        host: Server host address (default: 127.0.0.1)
        port: Server port number (default: 8000)
        log_level: Logging level for uvicorn (default: info)
    """
    
    host: str = Field(
        default="127.0.0.1", 
        description="Server host address"
    )
    port: int = Field(
        default=8000, 
        description="Server port number",
        ge=1,
        le=65535
    )
    log_level: str = Field(
        default="info", 
        description="Logging level (debug, info, warning, error, critical)"
    )
    
    def start(self, app: FastAPI):
        """
        Start the uvicorn server with the provided FastAPI application.
        
        Args:
            app: A configured FastAPI application instance
        """
        logger.info("="*50)
        logger.info(f"Starting BlogForge server")
        logger.info(f"Host: {self.host}")
        logger.info(f"Port: {self.port}")
        logger.info(f"Log Level: {self.log_level}")
        logger.info(f"API Docs: http://{self.host if self.host != '0.0.0.0' else 'localhost'}:{self.port}/docs")
        logger.info("="*50)
        
        # Run uvicorn server with the provided FastAPI instance
        uvicorn.run(
            app,
            host=self.host,
            port=self.port,
            log_level=self.log_level
        )