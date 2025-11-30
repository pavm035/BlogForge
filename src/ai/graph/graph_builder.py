from enum import Enum
from pydantic import BaseModel, Field
from langchain.chat_models import BaseChatModel
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.core import AppSession
from ..state.blog_state import BlogState
from ..node.blog_node import BlogNodeManager

class NodeId(str, Enum):        
    BLOG_AGENT = "blog_agent"    
    BLOG_WRITER = "blog_writer"
    SEARCH = "search"
    VALIDATE = "validate"
    TRANSLATE_BLOG = "translate_blog"

class BlogGraphBuilder(BaseModel):
    """
    A graph builder that constructs the blog generation workflow.
    
    This class creates a multi-node workflow graph for blog generation that includes:
    - Blog planning and topic analysis
    - Web search for relevant information
    - Content writing and generation
    - Content validation and quality checks
    - Translation support for multiple languages
    
    The graph uses conditional routing to handle different workflow paths
    based on user requirements and content validation results.
    """
    
    llm: BaseChatModel = Field(
        ...,
        description="An LLM instance (OpenAI, Anthropic, Groq, etc.)",
        exclude=True
    )
    
    app_session: AppSession = Field(
        ...,
        description="Application session instance with configuration"
    )
        
    def build(self) -> CompiledStateGraph:
        """
        Builds and compiles the blog generation graph with nodes and edges.
        
        Creates a complete workflow graph that orchestrates the blog generation process
        through multiple specialized nodes, each handling specific aspects of content
        creation, validation, and translation.
        
        Returns:
            CompiledStateGraph: A compiled LangGraph state graph ready for execution
            
        Raises:
            ValueError: If node manager initialization fails
            RuntimeError: If graph compilation fails
        """
        try:
            graph_builder = StateGraph(BlogState)
            
            # Initialize node manager with LLM and session configuration
            node_manager = BlogNodeManager(llm=self.llm, app_session=self.app_session)
        except Exception as e:
            raise ValueError(f"Failed to initialize graph components: {e}")
        
        graph_builder.add_node(NodeId.BLOG_AGENT.value, node_manager.blog_agent)
        graph_builder.add_node(NodeId.SEARCH.value, node_manager.tavily_multi_search)              
        graph_builder.add_node(NodeId.BLOG_WRITER.value, node_manager.blog_writer)        
        graph_builder.add_node(NodeId.VALIDATE.value, node_manager.validate_blog)
        graph_builder.add_node(NodeId.TRANSLATE_BLOG.value, node_manager.translate)
        
        # Add edges
        graph_builder.add_edge(START, NodeId.BLOG_AGENT.value)
        graph_builder.add_conditional_edges(
            NodeId.BLOG_AGENT.value,
            node_manager.tools_condition,
            {
                "tools": NodeId.SEARCH.value,
                "check_translation": NodeId.BLOG_WRITER.value
            },
        )
        
        graph_builder.add_edge(NodeId.SEARCH.value, NodeId.BLOG_WRITER.value)
        graph_builder.add_edge(NodeId.BLOG_WRITER.value, NodeId.VALIDATE.value)
        
        graph_builder.add_conditional_edges(
            NodeId.VALIDATE.value,
            node_manager.translate_condition,
            {
                "translate": NodeId.TRANSLATE_BLOG.value,
                "end": END
            }
        )
        graph_builder.add_edge(NodeId.TRANSLATE_BLOG.value, END)
        
        # Compile the graph with error handling
        try:
            compiled_graph = graph_builder.compile()
            return compiled_graph
        except Exception as e:
            raise RuntimeError(f"Failed to compile blog generation graph: {e}")
        