"""
Configuration Module

Centralized configuration for the Cricbuzz LiveStats application.
Includes database settings, API credentials, and app preferences.
"""

# Database Configuration
DB_TYPE = "sqlite"  # Options: sqlite, postgresql, mysql
DB_NAME = "cricbuzz.db"
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "user"
DB_PASSWORD = "password"

# API Configuration
CRICBUZZ_API_BASE_URL = "https://api.cricbuzz.com"
API_KEY = ""  # Set via environment variable

# Streamlit Configuration
PAGE_TITLE = "Cricbuzz LiveStats"
PAGE_ICON = "🏏"
LAYOUT = "wide"

# Data Validation
BATCH_SIZE = 100
QUERY_TIMEOUT = 30
