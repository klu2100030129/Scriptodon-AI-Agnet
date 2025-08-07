from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./scritodon.db"
    
    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = "your_openrouter_api_key_here"
    OPENROUTER_SITE_URL: str = "https://scritodon-backend.onrender.com"
    OPENROUTER_SITE_NAME: str = "Scriptodon Test Automation Platform"
    
    # Jira Configuration
    JIRA_SERVER_URL: str = "your_jira_server_url_here"
    JIRA_USERNAME: str = "your_jira_username_here"
    JIRA_API_TOKEN: str = "your_jira_api_token_here"
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://scritodon-frontend.onrender.com"
    ]
    
    class Config:
        env_file = ".env"

settings = Settings() 