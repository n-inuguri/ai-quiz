from src.llm.groq_client import get_groq_llm
from src.llm.openai_client import get_openai_llm
from src.config.settings import settings

def get_llm(provider: str, api_key: str, model: str, temperature: float = None):
    """
    Factory function to get the appropriate LLM based on provider.
    
    Args:
        provider: Model provider ('Groq' or 'OpenAI')
        api_key: API key for the selected provider
        model: Model name
        temperature: Sampling temperature (default: uses settings.TEMPERATURE)
    
    Returns:
        LLM instance (ChatGroq or ChatOpenAI)
    
    Raises:
        ValueError: If provider is not supported
    """
    if temperature is None:
        temperature = settings.TEMPERATURE
    
    if provider == "Groq":
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=api_key,
            model=model,
            temperature=temperature
        )
    elif provider == "OpenAI":
        return get_openai_llm(api_key, model, temperature)
    else:
        raise ValueError(f"Unsupported provider: {provider}")
