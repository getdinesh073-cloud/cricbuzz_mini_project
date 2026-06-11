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

# ==================== API Configuration (RapidAPI - Cricbuzz Cricket) ====================
# Using RapidAPI endpoint: https://rapidapi.com/api-sports/api/cricbuzz-cricket
CRICBUZZ_API_BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
CRICBUZZ_API_KEY = os.getenv("RAPIDAPI_KEY", "")
CRICBUZZ_API_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
API_RETRY_COUNT = int(os.getenv("API_RETRY_COUNT", "3"))

# API Endpoints
API_ENDPOINTS = {
    # Match endpoints
    "live_matches": "/matches/v1/live",
    "upcoming_matches": "/matches/v1/upcoming",
    "recent_matches": "/matches/v1/recent",
    "match_center": "/mcenter/v1/{match_id}",
    "match_scorecard": "/mcenter/v1/{match_id}/scard",
    "match_high_scorecard": "/mcenter/v1/{match_id}/hscard",
    "match_overs": "/mcenter/v1/{match_id}/overs",
    "match_team_data": "/mcenter/v1/{match_id}/team/{team_id}",
    
    # Series endpoints
    "international_series": "/series/v1/international",
    "series_archives": "/series/v1/archives/international",
    "series_details": "/series/v1/{series_id}",
    "series_squads": "/series/v1/{series_id}/squads",
    "series_squad_players": "/series/v1/{series_id}/squads/{team_id}",
    "series_venues": "/series/v1/{series_id}/venues",
    "series_points_table": "/stats/v1/series/{series_id}/points-table",
    "series_stats": "/stats/v1/series/{series_id}",
    
    # Team endpoints
    "international_teams": "/teams/v1/international",
    "team_schedule": "/teams/v1/{team_id}/schedule",
    "team_results": "/teams/v1/{team_id}/results",
    "team_players": "/teams/v1/{team_id}/players",
    "team_stats": "/stats/v1/team/{team_id}",
    
    # Player endpoints
    "player_trending": "/stats/v1/player/trending",
    "player_career": "/stats/v1/player/{player_id}/career",
    "player_bowling": "/stats/v1/player/{player_id}/bowling",
    "player_batting": "/stats/v1/player/{player_id}/batting",
    "player_search": "/stats/v1/player/search",
    
    # Rankings and standings
    "batting_rankings": "/stats/v1/rankings/batsmen",
    "bowling_rankings": "/stats/v1/rankings/bowlers",
    "icc_standing": "/stats/v1/iccstanding/team/matchtype/{matchtype}",
    
    # Top stats
    "top_stats": "/stats/v1/topstats",
    "top_stats_category": "/stats/v1/topstats/{category}",
}

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
        "api_host": CRICBUZZ_API_HOST,
        "timeout": API_TIMEOUT,
        "retry_count": API_RETRY_COUNT,
        "endpoints": API_ENDPOINTS,
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
