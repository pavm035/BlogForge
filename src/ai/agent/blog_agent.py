from pydantic import BaseModel, Field, model_validator, PrivateAttr
from langchain.chat_models import BaseChatModel
from langchain_core.runnables import Runnable

from src.core import AppSession
from ..graph.graph_builder import BlogGraphBuilder

class BlogAgent(BaseModel):
    """
    An agent class for generating blogs using LLM and graph workflows.
    
    This class encapsulates the blog generation logic by combining an LLM
    with a multi-node graph workflow for enhanced content creation.
    """
    
    llm: BaseChatModel = Field(
        ...,
        description="An LLM instance for blog generation"
    )
    
    app_session: AppSession = Field(
        ...,
        description="Application session instance with configuration"
    )
    
    _agent: Runnable = PrivateAttr()
    
    @model_validator(mode="after")
    def _post_init(self) -> "BlogAgent":
        """
        Initialize the agent after model validation.
        
        Returns:
            The initialized BlogAgent instance
        """
        self._agent = self._build()
        return self
            
    def _build(self) -> Runnable:
        """
        Builds the blog generation agent with the configured LLM and graph.
        
        Returns:
            A compiled graph agent ready for blog generation
            
        Raises:
            ValueError: If graph building fails
        """
        try:
            graph_builder = BlogGraphBuilder(llm=self.llm, app_session=self.app_session)
            agent = graph_builder.build()
            return agent
        except Exception as e:
            raise ValueError(f"Failed to build blog agent: {e}")
    
    @property
    def agent(self) -> Runnable:
        """Get the compiled graph agent ready for execution"""
        return self._agent