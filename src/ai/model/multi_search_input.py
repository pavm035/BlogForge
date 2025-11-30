from pydantic import BaseModel, Field

class MultiSearchInput(BaseModel):
    """Class to use for multiple search query with tavily"""
    
    queries: list[str] = Field(
        ..., 
        description="A mutiple queries for tavily search"
    )