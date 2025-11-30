from langchain.chat_models import init_chat_model, BaseChatModel
from pydantic import BaseModel, Field, model_validator, PrivateAttr, field_validator


class LLMManager(BaseModel):
    """Class that holds the LLM configuration and creates an LLM instance"""

    model: str = Field(
        ..., 
        description="The name of the LLM model"
    )

    model_provider: str | None = Field(
        default=None,
        description="The name of the model provider (e.g., openai, anthropic, groq)",
    )

    base_url: str | None = Field(
        default=None, 
        description="The gateway URL of the model provider (optional)"
    )
    
    ai_API_key: str = Field(
        ...,
        description="The API key for the AI service"
    )

    temperature: float = Field(
        default=0.7, 
        description="The temperature for the LLM (0.0 to 2.0)",
        ge=0.0,
        le=2.0
    )

    _llm: BaseChatModel = PrivateAttr()

    @field_validator('ai_API_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("API key cannot be empty")
        return v.strip()

    @model_validator(mode="after")
    def _post_init(self) -> "LLMManager":
        """
        Creates the LLM instance based on the given configuration.
        
        Raises:
            ValueError: If LLM initialization fails with the provided configuration
        """

        try:
            self._llm = init_chat_model(
                model=self.model,
                model_provider=self.model_provider,
                temperature=self.temperature,
                base_url=self.base_url,
                api_key=self.ai_API_key
            )
        except Exception as e:
            raise ValueError(f"Unable to create LLM with model '{self.model}' and provider '{self.model_provider}': {e}")
        
        return self
    
    @property
    def llm(self) -> BaseChatModel:
        """Get the initialized LLM instance"""
        return self._llm
