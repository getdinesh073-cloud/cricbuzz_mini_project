"""
Configuration Module

Centralized configuration for the Cricbuzz LiveStats application.
Includes database settings, API credentials, and app preferences.
Reads from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== Database Configuration ====================
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()  # Options: sqlite, postgresql, mysql
DB_NAME = os.getenv("DB_NAME", "cricbuzz.db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_TIMEOUT = int(os.getenv("DB_TIMEOUT", "30"))

# Validate database type
VALID_DB_TYPES = ["sqlite", "postgresql", "mysql"]
if DB_TYPE not in VALID_DB_TYPES:
    raise ValueError(f"DB_TYPE must be one of {VALID_DB_TYPES}, got {DB_TYPE}")

# ==================== API Configuration ====================
CRICBUZZ_API_BASE_URL = os.getenv(
    "CRICBUZZ_API_BASE_URL", 
    "https://api.cricbuzz.com/v1"
)
CRICBUZZ_API_KEY = os.getenv("CRICBUZZ_API_KEY", "")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))

# ==================== Streamlit Configuration ====================
PAGE_TITLE = "🏏 Cricbuzz LiveStats"
PAGE_ICON = "🏏"
LAYOUT = "wide"
THEME = "light"

# ==================== Data Processing ====================
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
QUERY_TIMEOUT = int(os.getenv("QUERY_TIMEOUT", "30"))
MAX_ROWS_DISPLAY = int(os.getenv("MAX_ROWS_DISPLAY", "1000"))

# ==================== Logging Configuration ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "cricbuzz_app.log")

# ==================== Application Settings ====================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
CACHE_DURATION = int(os.getenv("CACHE_DURATION", "300"))  # 5 minutes

# ==================== Validation ====================
def validate_config():
    """
    Validate critical configuration settings.
    Raises exception if required configs are missing or invalid.
    """
    if DB_TYPE in ["postgresql", "mysql"] and not all([DB_HOST, DB_USER, DB_PASSWORD]):
        raise ValueError(
            f"Database type {DB_TYPE} requires DB_HOST, DB_USER, and DB_PASSWORD"
        )
    
    if DEBUG:
        print(f"✓ Config loaded: DB_TYPE={DB_TYPE}, API_URL={CRICBUZZ_API_BASE_URL}")

# Run validation on import
try:
    validate_config()
except ValueError as e:
    print(f"⚠️  Config warning: {e}")

# ==================== Database Connection Strings ====================
def get_db_connection_string():
    """
    Generate appropriate database connection string based on DB_TYPE.
    
    Returns:
        str: Connection string or path for the selected database.
    """
    if DB_TYPE == "sqlite":
        return f"sqlite:///{DB_NAME}"
    elif DB_TYPE == "postgresql":
        return (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    elif DB_TYPE == "mysql":
        return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")

# ==================== Export Configuration ====================
CONFIG = {
    "database": {
        "type": DB_TYPE,
        "name": DB_NAME,
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "timeout": DB_TIMEOUT,
        "connection_string": get_db_connection_string(),
    },
    "api": {
        "base_url": CRICBUZZ_API_BASE_URL,
        "api_key": CRICBUZZ_API_KEY,
        "timeout": API_TIMEOUT,
        "retry_count": API_RETRY_COUNT,
    },
    "streamlit": {
        "page_title": PAGE_TITLE,
        "page_icon": PAGE_ICON,
        "layout": LAYOUT,
        "theme": THEME,
    },
    "app": {
        "debug": DEBUG,
        "log_level": LOG_LEVEL,
        "log_file": LOG_FILE,
        "cache_duration": CACHE_DURATION,
    },
}
