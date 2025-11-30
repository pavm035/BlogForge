import logging
import os
from typing import cast, Literal
from pydantic import BaseModel, Field, ValidationError

from langchain.chat_models import BaseChatModel
from langchain.messages import SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_tavily import TavilySearch
from langchain.tools import tool
from langgraph.prebuilt import ToolNode


from src.core import AppSession
from ..state.blog_state import BlogState, Blog
from ..model.multi_search_input import MultiSearchInput

logger = logging.getLogger(__name__)

class BlogNodeManager(BaseModel):
    """
    A blog node manager that creates and manages all workflow nodes.
    
    This class provides specialized nodes for the blog generation workflow,
    including content generation, search, writing, validation, and translation.
    Each node handles a specific aspect of the blog creation process.
    """

    llm: BaseChatModel = Field(
        ...,
        description="LLM instance for content generation (Groq, OpenAI, Anthropic, etc.)"
    )

    app_session: AppSession = Field(
        ...,
        description="Application session instance with configuration settings"
    )
    
    def blog_agent(self, state: BlogState) -> dict:
        """
        Generate multiple search queries for given topic or generate blog content directly.
        
        This method analyzes the topic and decides whether to use web search or
        generate content using the LLM's knowledge base.
        
        Args:
            state: A blog state provided by the agent during invocation
            
        Returns:
            Dict containing either search queries schema or blog content messages
            
        Raises:
            ValueError: If topic is invalid or content generation fails
        """
        
        logger.info("blog_agent method called")
        topic = state.get("topic")
        logger.info(f"Processing topic: {topic}")
        
        if not topic:
            raise ValueError("Invalid topic for the blog")
                
        system_prompt = f"""
            You are an expert in generating the blog for given topic {topic}.
            
            If you cannot generate the blog content with your existing knowledge, you can make a tavily tool call for search and ensure to generate the necessary schema {MultiSearchInput} with multiple queries.
            
            Guidelines:
            - Make only ONE tool call if needed
            - Generate 2-3 queries maximum for tavily search
            - Call tavily_multi_search when you need to search for information
            
            If you can generate the blog without tool calls, generate the content in the following format:
            {{
                "title": "Blog title in markdown",
                "content": "Detailed blog content in markdown"
            }}
        """
        messages = [
            SystemMessage(content=system_prompt)
        ]
        
        try:
            tools = [tavily_multi_search]
            llm_with_tools = self.llm.bind_tools(tools)
            response = llm_with_tools.invoke(messages)
            return {"messages": response}
        
        except ValidationError as e:
            logger.error(f"LLM generated invalid response: {e}")
            raise ValueError(f"Failed to generate valid response: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during content generation: {e}")
            raise ValueError(f"Failed to generate content: {e}")
            
    def tools_condition(self, state: BlogState) -> Literal["tools", "check_translation"]:
        """
        A decision router based on the generate_content output to transfer between either tools node or check_translation
        
        :param state: A blog state provided by agent during invocation
        :type state: BlogState
        :return: Returns next node as either `tools` or `check_translation`
        :rtype: Literal['tools', 'check_translation']
        """
        
        logger.info("tools_condition is called")
        messages = state.get("messages", [])
        
        if not messages:
            logger.error("Invalid messages to check for translation")
            raise ValueError("Invalid messages")
                        
        last_message = messages[-1]
        # logger.info(f"last_msg: {last_message.pretty_print()}")
        if isinstance(last_message, AIMessage) and len(last_message.tool_calls) > 0:
            return "tools"
        else:
            return "check_translation"
                    
    def tavily_multi_search(self, state: BlogState) -> ToolNode:
        """
        Tool node for tavily search operations.
        
        Args:
            state: Blog state containing search parameters
            
        Returns:
            A ToolNode for tavily search
        """
        
        return ToolNode([tavily_multi_search])
            
    def blog_writer(self, state: BlogState) -> dict:
        """
        A writer that generates a blog schema based on tavily search results or direct JSON content.
        
        This method processes either search results or direct content from the blog_agent
        and generates a structured blog with title and content.
        
        Args:
            state: A blog state provided by agent during invocation
        
        Returns:
            A valid blog schema with title and content
            
        Raises:
            ValueError: If messages are invalid or blog generation fails
        """
        
        logger.info("blog_writer method called")
        message_history = state.get("messages")
        if not message_history:
            logger.error("Messages can't be empty")
            raise ValueError("Invalid messages to generate a blog")
        
        last_message = message_history[-1].content
        
        if not last_message:
            logger.error("No valid message from AI to write a blog")
            raise ValueError("Invalid message to write a blog")
        
        system_prompt = f"""
            You are an expert blog writer. The input provided to you can be:
            - Tavily search results in format: {{"tavily_results": ...}}
            - Direct JSON blog response: {{"title": ..., "content": ...}}
            
            Generate a well-structured blog based on the following content:
            {last_message}
        """
        messages = [SystemMessage(content=system_prompt)]
        
        try:
            llm_with_structured_blog = self.llm.with_structured_output(Blog)
            blog = cast(Blog, llm_with_structured_blog.invoke(messages))
            logger.info(f"Generated a valid blog object with title: {blog.title}")
            return {"blog": blog}        
        except ValidationError as e:
            logger.error(f"LLM generated invalid blog: {e}")
            raise ValueError(f"Failed to generate valid blog: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during content generation: {e}")
            raise ValueError(f"Failed to generate content: {e}")
                                                                
    def validate_blog(self, state: BlogState) -> dict:
        """
        Validates the generated blog content.
        
        Args:
            state: A blog state provided by agent during invocation
            
        Returns:
            Validated blog state
            
        Raises:
            ValueError: If blog is invalid
        """
        
        logger.info("validate_blog method called")
        generated_blog = state.get("blog")
        
        if not generated_blog:
            logger.error("Invalid blog to perform validation")
            raise ValueError("Invalid blog for validation")        
        
        return {**state}
    
    def translate_condition(self, state: BlogState) -> Literal["translate", "end"]:
        """
        A router that routes between translate node or end

        If there is no language provided then it raises an excpeption

        Args:
            state: A blog state provided by agent during invocation

        Returns:
            A decision to go to next node
        """

        logger.info("translate_condition is called")
        language = state.get("language", "")
        language_name = self.app_session.get_language_name(language)
        logger.info(f"requested language: {language}, language_name: {language_name}")

        if not (language or language_name):
            logger.error("Invalid language")
            raise ValueError("Language must be provided for translation")

        if language == "en":
            logger.info(f"Skipping translation because requested language is default (en)")
            return "end"
        else:            
            return "translate"
        
    def translate(self, state: BlogState) -> dict:
        """
        Translates the generated blog into the requested language.
        
        Args:
            state: A blog state provided by agent during invocation
            
        Returns:
            A translated blog with title and content
            
        Raises:
            ValueError: If blog or language is invalid
        """

        logger.info("translate method called")
        blog = state.get("blog")
        language = state.get("language", "")
        language_name = self.app_session.get_language_name(language)
        
        if blog is None:
            logger.error("Invalid blog to translate")
            raise ValueError("Invalid blog to translate, check again")

        if not language or not language_name:
            logger.error("Invalid/unsupported language for translation")
            raise ValueError("Invalid language to translate, check again")        

        logger.info(f"Translating a blog in: {language}, language_name: {language_name}")
        
        try:                                               
            system_msg = SystemMessage(
                content="""
                You are an expert in translating blog to the user's requested language.
                Translate accurately with no preamble or additional commentary.
                
                If you are unable to translate, raise an exception with an appropriate error message.
                
                Use the provided blog content to translate and produce structured output
                with the same blog schema in markdown format.
                """
            )

            human_msg = HumanMessage(
                content=f"""
                Please translate the following blog:
                
                Blog content: {blog}
                
                Target language: {language} ({language_name})
                """
            )            
            messages = [system_msg, human_msg]

            llm_with_blog_fmt = self.llm.with_structured_output(Blog)            
            translated_blog = cast(Blog, llm_with_blog_fmt.invoke(messages))
            logger.info(f"Translated a blog: {translated_blog} in {language}")
            return {"blog": translated_blog}

        except ValidationError as e:
            logger.error(f"LLM translated invalid blog data: {e}")
            raise ValueError(f"Failed to translate valid blog content: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during blog translation: {e}")
            raise ValueError(f"Failed to translate blog: {e}")
        


# Tools
@tool("tavily_multi_search")
def tavily_multi_search(input: MultiSearchInput) -> dict:
    """
    Performs batch tavily search with given input and returns search results.
    
    Args:
        input: A multi-query search input containing search queries
        
    Returns:
        A dictionary containing a list of tavily search results
        
    Raises:
        ValueError: If TAVILY_API_KEY is not found in environment variables
    """
    
    logger.info(f"tavily_multi_search called with input: {input}")
    
    # Get Tavily API key from environment
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    
    tavily_client = TavilySearch(api_key=tavily_api_key, max_results=2)
    tavily_results: list[dict] = []
    
    for q in input.queries:            
        logger.info(f"Performing tavily search for: {q}")
        
        search_results = tavily_client.invoke({"query": q})
        tavily_results.append({"query": q, "results": search_results})
        
    return {"tavily_results": tavily_results}
    