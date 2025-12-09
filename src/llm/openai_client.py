from langchain_openai import ChatOpenAI

def get_openai_llm(api_key: str, model: str, temperature: float = 0.9):
    """
    Create and return an OpenAI LLM instance.
    
    Args:
        api_key: OpenAI API key
        model: Model name (e.g., 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo')
        temperature: Sampling temperature (default: 0.9)
    
    Returns:
        ChatOpenAI instance
    """
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature
    )
