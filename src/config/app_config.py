import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    # API Keys
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

    AZURE_GROK_API_KEY = os.getenv("AZURE_GROK_API_KEY")
    AZURE_GROK_ENDPOINT = os.getenv("AZURE_GROK_ENDPOINT")
    AZURE_GROK_DEPLOYMENT = os.getenv("AZURE_GROK_DEPLOYMENT")
    AZURE_GROK_MODEL = os.getenv("AZURE_GROK_MODEL")
    AZURE_GROK_API_VERSION = os.getenv("AZURE_GROK_API_VERSION")

    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    CORS_ORIGINS = ["*"]

    # Search settings
    MAX_SEARCH_RESULTS: int = 20
    SEARCH_TIMEOUT: int = 60
    MAX_SEARCH_ITERATIONS: int = 10

    # Analysis settings
    CONFIDENCE_THRESHOLD: float = 0.6
    RISK_SEVERITY_LEVELS: list = None

    def __post_init__(self):
        if self.RISK_SEVERITY_LEVELS is None:
            self.RISK_SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def validate_config(self):
        """Validate that required API keys are present"""
        required_keys = []

        # Only validate keys that are actually used in services.py
        if not self.AZURE_OPENAI_API_KEY:
            required_keys.append("AZURE_OPENAI_API_KEY")
        if not self.AZURE_OPENAI_ENDPOINT:
            required_keys.append("AZURE_OPENAI_ENDPOINT")
        if not self.AZURE_OPENAI_DEPLOYMENT:
            required_keys.append("AZURE_OPENAI_DEPLOYMENT")
        if not self.AZURE_OPENAI_MODEL:
            required_keys.append("AZURE_OPENAI_MODEL")
        if not self.AZURE_OPENAI_API_VERSION:
            required_keys.append("AZURE_OPENAI_API_VERSION")

        if not self.AZURE_GROK_API_KEY:
            required_keys.append("AZURE_GROK_API_KEY")
        if not self.AZURE_GROK_ENDPOINT:
            required_keys.append("AZURE_GROK_ENDPOINT")
        if not self.AZURE_GROK_DEPLOYMENT:
            required_keys.append("AZURE_GROK_DEPLOYMENT")
        if not self.AZURE_GROK_MODEL:
            required_keys.append("AZURE_GROK_MODEL")
        if not self.AZURE_GROK_API_VERSION:
            required_keys.append("AZURE_GROK_API_VERSION")

        if not self.TAVILY_API_KEY:
            required_keys.append("TAVILY_API_KEY")

        if required_keys:
            raise ValueError(f"Missing required API keys: {', '.join(required_keys)}")

        return True


# Global config instance
config = Config()
