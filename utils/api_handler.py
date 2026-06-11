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
    Make HTTP request to Cricbuzz API (RapidAPI) with error handling.
    
    Args:
        endpoint (str): API endpoint (already includes /matches/v1, /mcenter/v1, etc).
        method (str): HTTP method (GET, POST, etc.).
        params (dict): Query parameters.
        json_data (dict): JSON request body.
        
    Returns:
        dict: JSON response or None if error.
    """
    try:
        # RapidAPI headers
        headers = {
            "x-rapidapi-key": config.CRICBUZZ_API_KEY,
            "x-rapidapi-host": config.CRICBUZZ_API_HOST,
            "Content-Type": "application/json",
        }
        
        url = f"{config.CRICBUZZ_API_BASE_URL}{endpoint}"
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
    Uses endpoint: /matches/v1/live
    
    Returns:
        List of live match data or None if error.
    """
    try:
        logger.info("Fetching live matches...")
        endpoint = config.API_ENDPOINTS.get("live_matches", "/matches/v1/live")
        data = _make_request(endpoint)
        
        if data:
            matches = data.get("matches", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(matches)} live matches")
            return matches
        return None
        
    except Exception as e:
        logger.error(f"✗ Failed to fetch live matches: {str(e)}")
        return None


def fetch_match_scorecard(match_id: str) -> Optional[Dict]:
    """
    Fetch detailed scorecard for a specific match.
    Uses endpoint: /mcenter/v1/{match_id}/scard
    
    Args:
        match_id (str): Match ID from Cricbuzz API.
        
    Returns:
        Match scorecard details or None if error.
    """
    try:
        logger.info(f"Fetching scorecard for match {match_id}...")
        endpoint_template = config.API_ENDPOINTS.get("match_scorecard", "/mcenter/v1/{match_id}/scard")
        endpoint = endpoint_template.format(match_id=match_id)
        data = _make_request(endpoint)
        
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
    Uses endpoints: /stats/v1/player/trending or /stats/v1/player/{player_id}/career
    
    Args:
        player_id (str, optional): Specific player ID. If None, fetch trending players.
        
    Returns:
        Player statistics data or None if error.
    """
    try:
        logger.info(f"Fetching player stats..." + (f" for {player_id}" if player_id else ""))
        
        if player_id:
            endpoint_template = config.API_ENDPOINTS.get("player_career", "/stats/v1/player/{player_id}/career")
            endpoint = endpoint_template.format(player_id=player_id)
        else:
            endpoint = config.API_ENDPOINTS.get("player_trending", "/stats/v1/player/trending")
        
        data = _make_request(endpoint)
        
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
    Uses endpoints: /series/v1/international or /series/v1/{series_id}
    
    Args:
        series_id (str, optional): Specific series ID. If None, fetch international series.
        
    Returns:
        Series data including teams and match schedules.
    """
    try:
        logger.info(f"Fetching series info..." + (f" for {series_id}" if series_id else ""))
        
        if series_id:
            endpoint_template = config.API_ENDPOINTS.get("series_details", "/series/v1/{series_id}")
            endpoint = endpoint_template.format(series_id=series_id)
        else:
            endpoint = config.API_ENDPOINTS.get("international_series", "/series/v1/international")
        
        data = _make_request(endpoint)
        
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
    Uses endpoint: /stats/v1/team/{team_id}
    
    Args:
        team_id (str): Team ID.
        
    Returns:
        Team statistics or None if error.
    """
    try:
        logger.info(f"Fetching team stats for {team_id}...")
        endpoint_template = config.API_ENDPOINTS.get("team_stats", "/stats/v1/team/{team_id}")
        endpoint = endpoint_template.format(team_id=team_id)
        data = _make_request(endpoint)
        
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
    Uses endpoint: /series/v1/{series_id}/venues (requires series_id)
    
    Returns:
        List of venues or None if error.
    """
    try:
        logger.info("Fetching venues...")
        # Default to fetching venues for series 3718 (example)
        endpoint_template = config.API_ENDPOINTS.get("series_venues", "/series/v1/{series_id}/venues")
        endpoint = endpoint_template.format(series_id="3718")
        data = _make_request(endpoint)
        
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
    Uses endpoint: /matches/v1/live
    
    Returns:
        bool: True if API is reachable, False otherwise.
    """
    try:
        logger.info("Testing API connection...")
        endpoint = config.API_ENDPOINTS.get("live_matches", "/matches/v1/live")
        data = _make_request(endpoint, method="GET")
        
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


# ==================== Additional API Functions ====================

def fetch_upcoming_matches() -> Optional[List[Dict]]:
    """Fetch upcoming matches."""
    try:
        logger.info("Fetching upcoming matches...")
        endpoint = config.API_ENDPOINTS.get("upcoming_matches", "/matches/v1/upcoming")
        data = _make_request(endpoint)
        if data:
            matches = data.get("matches", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(matches)} upcoming matches")
            return matches
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch upcoming matches: {str(e)}")
        return None


def fetch_recent_matches() -> Optional[List[Dict]]:
    """Fetch recent matches."""
    try:
        logger.info("Fetching recent matches...")
        endpoint = config.API_ENDPOINTS.get("recent_matches", "/matches/v1/recent")
        data = _make_request(endpoint)
        if data:
            matches = data.get("matches", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(matches)} recent matches")
            return matches
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch recent matches: {str(e)}")
        return None


def fetch_match_data(match_id: str) -> Optional[Dict]:
    """Fetch detailed match center data."""
    try:
        logger.info(f"Fetching match data for {match_id}...")
        endpoint_template = config.API_ENDPOINTS.get("match_center", "/mcenter/v1/{match_id}")
        endpoint = endpoint_template.format(match_id=match_id)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved match data for {match_id}")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch match data: {str(e)}")
        return None


def fetch_match_overs(match_id: str) -> Optional[Dict]:
    """Fetch match overs data."""
    try:
        logger.info(f"Fetching overs for match {match_id}...")
        endpoint_template = config.API_ENDPOINTS.get("match_overs", "/mcenter/v1/{match_id}/overs")
        endpoint = endpoint_template.format(match_id=match_id)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved overs for match {match_id}")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch match overs: {str(e)}")
        return None


def fetch_match_team_data(match_id: str, team_id: str) -> Optional[Dict]:
    """Fetch team data for a specific match."""
    try:
        logger.info(f"Fetching team {team_id} data for match {match_id}...")
        endpoint_template = config.API_ENDPOINTS.get("match_team_data", "/mcenter/v1/{match_id}/team/{team_id}")
        endpoint = endpoint_template.format(match_id=match_id, team_id=team_id)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved team data for match {match_id}")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch team data: {str(e)}")
        return None


def fetch_series_squads(series_id: str) -> Optional[Dict]:
    """Fetch squads for a series."""
    try:
        logger.info(f"Fetching squads for series {series_id}...")
        endpoint_template = config.API_ENDPOINTS.get("series_squads", "/series/v1/{series_id}/squads")
        endpoint = endpoint_template.format(series_id=series_id)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved squads for series {series_id}")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch series squads: {str(e)}")
        return None


def fetch_series_points_table(series_id: str) -> Optional[Dict]:
    """Fetch points table for a series."""
    try:
        logger.info(f"Fetching points table for series {series_id}...")
        endpoint_template = config.API_ENDPOINTS.get("series_points_table", "/stats/v1/series/{series_id}/points-table")
        endpoint = endpoint_template.format(series_id=series_id)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved points table for series {series_id}")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch points table: {str(e)}")
        return None


def fetch_international_teams() -> Optional[List[Dict]]:
    """Fetch international teams."""
    try:
        logger.info("Fetching international teams...")
        endpoint = config.API_ENDPOINTS.get("international_teams", "/teams/v1/international")
        data = _make_request(endpoint)
        if data:
            teams = data.get("teams", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(teams)} international teams")
            return teams
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch teams: {str(e)}")
        return None


def fetch_team_schedule(team_id: str) -> Optional[List[Dict]]:
    """Fetch team schedule."""
    try:
        logger.info(f"Fetching schedule for team {team_id}...")
        endpoint_template = config.API_ENDPOINTS.get("team_schedule", "/teams/v1/{team_id}/schedule")
        endpoint = endpoint_template.format(team_id=team_id)
        data = _make_request(endpoint)
        if data:
            matches = data.get("schedule", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved schedule for team {team_id}")
            return matches
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch team schedule: {str(e)}")
        return None


def fetch_team_results(team_id: str) -> Optional[List[Dict]]:
    """Fetch team results."""
    try:
        logger.info(f"Fetching results for team {team_id}...")
        endpoint_template = config.API_ENDPOINTS.get("team_results", "/teams/v1/{team_id}/results")
        endpoint = endpoint_template.format(team_id=team_id)
        data = _make_request(endpoint)
        if data:
            results = data.get("results", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved results for team {team_id}")
            return results
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch team results: {str(e)}")
        return None


def fetch_team_players(team_id: str) -> Optional[List[Dict]]:
    """Fetch team players."""
    try:
        logger.info(f"Fetching players for team {team_id}...")
        endpoint_template = config.API_ENDPOINTS.get("team_players", "/teams/v1/{team_id}/players")
        endpoint = endpoint_template.format(team_id=team_id)
        data = _make_request(endpoint)
        if data:
            players = data.get("players", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved {len(players)} players for team {team_id}")
            return players
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch team players: {str(e)}")
        return None


def fetch_player_search(player_name: str) -> Optional[List[Dict]]:
    """Search for players by name."""
    try:
        logger.info(f"Searching for player: {player_name}...")
        endpoint = config.API_ENDPOINTS.get("player_search", "/stats/v1/player/search")
        params = {"plrN": player_name}
        data = _make_request(endpoint, params=params)
        if data:
            results = data.get("players", []) if isinstance(data, dict) else data
            logger.info(f"✓ Found {len(results) if isinstance(results, list) else 'some'} players")
            return results
        return None
    except Exception as e:
        logger.error(f"✗ Failed to search players: {str(e)}")
        return None


def fetch_batting_rankings(format_type: str = "test") -> Optional[List[Dict]]:
    """Fetch batting rankings for format (test/odi/t20i)."""
    try:
        logger.info(f"Fetching batting rankings for {format_type}...")
        endpoint = config.API_ENDPOINTS.get("batting_rankings", "/stats/v1/rankings/batsmen")
        params = {"formatType": format_type}
        data = _make_request(endpoint, params=params)
        if data:
            rankings = data.get("rankings", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved batting rankings")
            return rankings
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch batting rankings: {str(e)}")
        return None


def fetch_bowling_rankings(format_type: str = "test") -> Optional[List[Dict]]:
    """Fetch bowling rankings for format (test/odi/t20i)."""
    try:
        logger.info(f"Fetching bowling rankings for {format_type}...")
        endpoint = config.API_ENDPOINTS.get("bowling_rankings", "/stats/v1/rankings/bowlers")
        params = {"formatType": format_type}
        data = _make_request(endpoint, params=params)
        if data:
            rankings = data.get("rankings", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved bowling rankings")
            return rankings
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch bowling rankings: {str(e)}")
        return None


def fetch_top_stats(category: str = "0", stats_type: str = "mostRuns") -> Optional[List[Dict]]:
    """Fetch top statistics for category."""
    try:
        logger.info(f"Fetching top stats for category {category}...")
        endpoint_template = config.API_ENDPOINTS.get("top_stats_category", "/stats/v1/topstats/{category}")
        endpoint = endpoint_template.format(category=category)
        params = {"statsType": stats_type}
        data = _make_request(endpoint, params=params)
        if data:
            stats = data.get("stats", []) if isinstance(data, dict) else data
            logger.info(f"✓ Retrieved top stats")
            return stats
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch top stats: {str(e)}")
        return None


def fetch_icc_standings(matchtype: int = 1) -> Optional[Dict]:
    """Fetch ICC standings for match type (1=Test, 2=ODI, 3=T20I)."""
    try:
        logger.info(f"Fetching ICC standings for matchtype {matchtype}...")
        endpoint_template = config.API_ENDPOINTS.get("icc_standing", "/stats/v1/iccstanding/team/matchtype/{matchtype}")
        endpoint = endpoint_template.format(matchtype=matchtype)
        data = _make_request(endpoint)
        if data:
            logger.info(f"✓ Retrieved ICC standings")
            return data
        return None
    except Exception as e:
        logger.error(f"✗ Failed to fetch ICC standings: {str(e)}")
        return None
