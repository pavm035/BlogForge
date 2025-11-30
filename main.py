from dotenv import load_dotenv
import logging
import sys

# Load environment variables FIRST, before any other imports
load_dotenv()

from src.core import AppSession
from src.api.api import BlogAPIManager
from src.app import BlogApp

logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the BlogForge application.
    
    Initializes the application session, API manager, and starts
    the FastAPI server with uvicorn.
    """
    try:
        logger.info("Initializing BlogForge application...")
        
        # Create app session with environment configuration
        app_session = AppSession()
        logger.info(f"Using model: {app_session.model_name} from provider: {app_session.model_provider}")
        
        # Create API manager with custom configuration
        api_manager = BlogAPIManager(
            model_name=app_session.model_name,
            model_provider=app_session.model_provider,
            base_url=app_session.ai_base_url,
            ai_API_key=app_session.ai_API_key,
            api_title="BlogForge API",
            api_description="AI-powered blog generation service with multi-language support",
            app_session=app_session
        )
        
        # Create and start the app
        blog_app = BlogApp(
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
        blog_app.start(api_manager.api)
        
    except KeyboardInterrupt:
        logger.info("\nShutting down BlogForge application...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start BlogForge application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
