"""
Cricbuzz API Handler Module

Handles all REST API calls to Cricbuzz API for fetching:
- Live match data
- Player statistics
- Series information
- Match updates and scorecards
"""

import logging
import requests
from typing import Dict, List, Optional
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

# Create session with retry strategy
def create_session():
    """
    Create a requests session with retry strategy.
    
    Returns:
        requests.Session: Session object with retries configured.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=config.API_RETRY_COUNT,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


session = create_session()


def _make_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None
) -> Optional[Dict]:
    """
    Make HTTP request to Cricbuzz API with error handling.
    
    Args:
        endpoint (str): API endpoint (without base URL).
        method (str): HTTP method (GET, POST, etc.).
        params (dict): Query parameters.
        json_data (dict): JSON request body.
        
    Returns:
        dict: JSON response or None if error.
    """
    try:
        headers = {
            "User-Agent": "Cricbuzz-LiveStats/1.0",
            "Content-Type": "application/json",
        }
        
        if config.CRICBUZZ_API_KEY:
            headers["Authorization"] = f"Bearer {config.CRICBUZZ_API_KEY}"
        
        url = f"{config.CRICBUZZ_API_BASE_URL}/{endpoint}"
        logger.debug(f"Requesting: {method} {url}")
        
        response = session.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_data,
            timeout=config.API_TIMEOUT
        )
        
        response.raise_for_status()
        logger.info(f"✓ {method} {endpoint} - Status {response.status_code}")
        
        return response.json()
        
    except requests.exceptions.Timeout:
        logger.error(f"✗ API request timeout: {endpoint}")
        return None
    except requests.exceptions.ConnectionError:
        logger.error(f"✗ Connection error: {endpoint}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"✗ HTTP error {e.response.status_code}: {endpoint}")
        return None
    except ValueError:
        logger.error(f"✗ Invalid JSON response: {endpoint}")
        return None
    except Exception as e:
        logger.error(f"✗ API error: {str(e)}")
        return None


def fetch_live_matches() -> Optional[List[Dict]]:
    """
    Fetch ongoing matches from Cricbuzz API.
    
    Returns:
        List of live match data or None if error.
    """
    try:
        logger.info("Fetching live matches...")
        data = _make_request("matches/live")
        
        if data:
            matches = data.get("matches", [])
            logger.info(f"✓ Retrieved {len(matches)} live matches")
            return matches
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch live matches: {str(e)}")
        return None


def fetch_match_scorecard(match_id: str) -> Optional[Dict]:
    """
    Fetch detailed scorecard for a specific match.
    
    Args:
        match_id (str): Match ID from Cricbuzz API.
        
    Returns:
        Match scorecard details or None if error.
    """
    try:
        logger.info(f"Fetching scorecard for match {match_id}...")
        data = _make_request(f"matches/{match_id}")
        
        if data:
            logger.info(f"✓ Retrieved scorecard for match {match_id}")
            return data
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch scorecard: {str(e)}")
        return None


def fetch_player_stats(player_id: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Fetch player statistics from Cricbuzz API.
    
    Args:
        player_id (str, optional): Specific player ID. If None, fetch all top players.
        
    Returns:
        Player statistics data or None if error.
    """
    try:
        logger.info(f"Fetching player stats..." + (f" for {player_id}" if player_id else ""))
        
        if player_id:
            data = _make_request(f"players/{player_id}")
        else:
            data = _make_request("players/stats")
        
        if data:
            stats = data.get("stats", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved player statistics")
            return stats
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch player stats: {str(e)}")
        return None


def fetch_series_info(series_id: Optional[str] = None) -> Optional[Dict]:
    """
    Fetch series information from Cricbuzz API.
    
    Args:
        series_id (str, optional): Specific series ID. If None, fetch current series.
        
    Returns:
        Series data including teams and match schedules.
    """
    try:
        logger.info(f"Fetching series info..." + (f" for {series_id}" if series_id else ""))
        
        if series_id:
            data = _make_request(f"series/{series_id}")
        else:
            data = _make_request("series/current")
        
        if data:
            logger.info(f"✓ Retrieved series information")
            return data
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch series info: {str(e)}")
        return None


def fetch_team_stats(team_id: str) -> Optional[Dict]:
    """
    Fetch team statistics from Cricbuzz API.
    
    Args:
        team_id (str): Team ID.
        
    Returns:
        Team statistics or None if error.
    """
    try:
        logger.info(f"Fetching team stats for {team_id}...")
        data = _make_request(f"teams/{team_id}")
        
        if data:
            logger.info(f"✓ Retrieved team statistics")
            return data
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch team stats: {str(e)}")
        return None


def fetch_venues() -> Optional[List[Dict]]:
    """
    Fetch all cricket venues from Cricbuzz API.
    
    Returns:
        List of venues or None if error.
    """
    try:
        logger.info("Fetching venues...")
        data = _make_request("venues")
        
        if data:
            venues = data.get("venues", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(venues)} venues")
            return venues
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch venues: {str(e)}")
        return None


def test_api_connection() -> bool:
    """
    Test API connection with a simple request.
    
    Returns:
        bool: True if API is reachable, False otherwise.
    """
    try:
        logger.info("Testing API connection...")
        data = _make_request("health", method="GET")
        
        if data:
            logger.info("✓ API connection successful")
            return True
        logger.warning("⚠ API connection test failed")
        return False
        
    except Exception as e:
        logger.error(f"✗ API connection test failed: {str(e)}")
        return False


def handle_api_error(error: Exception) -> Dict:
    """
    Handle and format API errors gracefully.
    
    Args:
        error (Exception): Exception from API call.
        
    Returns:
        dict: Error information formatted for display.
    """
    error_info = {
        "status": "error",
        "message": str(error),
        "type": type(error).__name__,
    }
    
    logger.error(f"API Error: {error_info}")
    return error_info
