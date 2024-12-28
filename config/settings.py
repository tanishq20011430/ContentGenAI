import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    DATA_DIR = 'data'
    ALLOWED_DOMAINS = ['example.com', 'trusted-domain.com']
    HISTORY_FILE = 'content_history.json'
    RATE_LIMIT_DELAY = 1
    MAX_RETRIES = 3
    TIMEOUT = 30