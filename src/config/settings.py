import os
from dotenv import load_dotenv

load_dotenv()

class Settings():

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Default model settings (deprecated - now using session-based selection)
    MODEL_NAME = "llama-3.1-8b-instant"
    
    TEMPERATURE = 0.9

    MAX_RETRIES = 3

    # Available models for each provider
    GROQ_MODELS = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]

    OPENAI_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo"
    ]

    MODEL_PROVIDERS = ["Groq", "OpenAI"]

    # Persona configurations
    PERSONAS = {
        "Friendly Tutor": {
            "name": "Friendly Tutor",
            "icon": "🎓",
            "description": "An encouraging, patient tutor who provides helpful hints and context. Focuses on understanding concepts.",
            "style": "encouraging and supportive with clear explanations"
        },
        "Strict Examiner": {
            "name": "Strict Examiner",
            "icon": "📝",
            "description": "A formal, challenging examiner who tests precise knowledge and details with no-nonsense questions.",
            "style": "formal and challenging, testing precise knowledge"
        },
        "Playful Coach": {
            "name": "Playful Coach",
            "icon": "🎮",
            "description": "A fun, gamified coach who uses analogies and real-world examples to make learning engaging.",
            "style": "fun and engaging with real-world examples and analogies"
        },
        "Custom": {
            "name": "Custom",
            "icon": "✨",
            "description": "Define your own persona for a unique learning experience.",
            "style": None  # Will be user-defined
        }
    }

    PERSONA_OPTIONS = list(PERSONAS.keys())


settings = Settings()  