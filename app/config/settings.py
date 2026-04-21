# Config settings

import os 
from dotenv import load_dotenv
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=_ROOT / '.env', override=False)


GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')


CHROMA_DIR = os.getenv('CHROMA_DIR', str(_ROOT / 'chroma_db'))
CHROMA_NAME: str = "bot_personas"

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'models/gemini-embedding-001')

ROUTING_THRESHOLD: float = float(os.getenv('ROUTING_THRESHOLD', '0.5'))


# Validation 

def validate_settings() -> None:
    if not GROQ_API_KEY:
        raise EnvironmentError("GROQ_API_KEY is not set in environment variables.")
    if not GOOGLE_API_KEY:
        raise EnvironmentError("GOOGLE_API_KEY is not set in environment variables.")

if __name__ == "__main__":
    validate_settings()
    print("All settings are valid.")