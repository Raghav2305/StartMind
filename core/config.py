# core/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file variables

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = "gpt-4"
    VECTOR_DB_PATH = "vector_db/"
