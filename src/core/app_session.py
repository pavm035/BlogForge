import os
from pydantic import BaseModel, Field


class AppSession(BaseModel):
    """
    A general session for the app
    """

    supported_languages: dict[str, str] = Field(
        default={
            "en": "english",
            "ja": "japanese", 
            "fr": "french",
            "hi": "hindi",
            "kn": "kannada",
            "te": "telugu",
            "zh": "chinese"
        },
        description="A mapping of language codes to language names for blog generation",
        exclude=True,
    )
    
    def get_language_name(self, code: str) -> str | None:
        """
            Returns the language name for supported language based on code
            
            Args:
                - code: A language code
            
            Returns:
                Language name if exists else None
        """
    
        return self.supported_languages.get(code)
    
    # Model info from env
    @property
    def model_name(self) -> str:
        model = os.getenv("MODEL_NAME")
        
        if not model:
            raise ValueError("MODEL_NAME can't be blank, please configure in .env file")
        return model
    
    @property
    def model_provider(self) -> str:        
        model_provider = os.getenv("MODEL_PROVIDER")
        
        if not model_provider:
            raise ValueError("MODEL_PROVIDER can't be blank, please configure in .env file")
        return model_provider
    
    @property
    def ai_base_url(self) -> str | None:
        return os.getenv("AI_BASE_URL")
    
    @property
    def ai_API_key(self) -> str:        
        api_key = os.getenv("AI_API_KEY")
        if not api_key:
            raise ValueError("AI_API_KEY can't be blank, please configure in .env file")
        return api_key
    
    
    
