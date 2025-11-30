from typing import TypedDict, NotRequired, Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import BaseMessage, add_messages

class Blog(BaseModel):
    title: str = Field(..., description="The title of the blog", min_length=5)
    content: str = Field(default="", description="The detailed content of the blog")

class BlogState(TypedDict):
    """State that holds the information about blog"""
    topic: str
    blog: NotRequired[Blog]
    language: str
    messages: NotRequired[Annotated[list[BaseMessage], add_messages]]
    tavily_results: NotRequired[list[dict]]

    
    