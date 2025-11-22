import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    # LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    # LANGCHAIN_TRACING = os.getenv("LANGCHAIN_TRACING", "true")
    # LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "DocChat")
    
    # Pinecone Settings
    PINECONE_INDEX_NAME = "dense-langchain"
    PINECONE_CLOUD = "aws"
    PINECONE_REGION = "us-east-1"
    
    # Model Settings
    GEMINI_MODEL = "gemini-2.0-flash" 
    EMBEDDING_MODEL = "models/gemini-embedding-001"

settings = Settings()