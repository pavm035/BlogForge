"""
LangGraph Studio entry point for BlogForge
"""

from dotenv import load_dotenv

from src.core import AppSession
from src.ai.llm.llm_manager import LLMManager
from src.ai.graph.graph_builder import BlogGraphBuilder

def create_graph():
    """
    Factory function for LangGraph Studio
    Creates and returns a compiled graph
    """
    
    load_dotenv()
    app_session: AppSession = AppSession()
    
    # Initialize LLM Manager
    llm_manager = LLMManager(
        model=app_session.model_name, 
        model_provider=app_session.model_provider,
        base_url=app_session.ai_base_url,
        ai_API_key=app_session.ai_API_key
    )
    
    # Create graph builder
    graph_builder = BlogGraphBuilder(llm=llm_manager.llm, app_session=app_session)
    
    # Build and return compiled graph
    return graph_builder.build()

# This is what LangGraph Studio will import
graph = create_graph()