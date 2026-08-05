import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
    STORAGE_PATH = os.getenv("STORAGE_PATH", "app/storage")

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SKILLS_DIR = os.path.join(BASE_DIR, "skills")
    AGENTS_DIR = os.path.join(BASE_DIR, "agents")
    SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

settings = Settings()