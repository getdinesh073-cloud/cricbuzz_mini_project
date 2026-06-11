"""
Live Matches Page

Displays real-time cricket matches with live scorecards, player info, and venue details.
Data fetched from Cricbuzz API.
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime

from utils import api_handler

logger = logging.getLogger(__name__)


def display_header():
    """Display page header."""
    st.markdown("# ⚡ Live Matches")
    st.markdown("Real-time cricket matches from Cricbuzz API")
    st.markdown("---")


@st.cache_data(ttl=300)
def fetch_matches():
    """
    Fetch live matches from API (cached for 5 minutes).
    
    Returns:
        list: List of matches or empty list if error.
    """
    try:
        matches = api_handler.fetch_live_matches()
        if matches:
            logger.info(f"✓ Fetched {len(matches)} live matches")
            return matches
        return []
    except Exception as e:
        logger.error(f"✗ Failed to fetch matches: {str(e)}")
        return []


def display_match_card(match):
    """
    Display a single match card with formatted information.
    
    Args:
        match (dict): Match data from API.
    """
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        # Match status indicator
        with col1:
            status = match.get("status", "Not Started").upper()
            if "LIVE" in status:
                st.markdown("<span style='color: #ff4444; font-weight: bold;'>🔴 LIVE</span>", unsafe_allow_html=True)
            elif "COMPLETED" in status:
                st.markdown("<span style='color: #44aa44; font-weight: bold;'>✓ COMPLETED</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: #888; font-weight: bold;'>⏱ UPCOMING</span>", unsafe_allow_html=True)
        
        # Match details
        with col2:
            st.markdown(f"### {match.get('description', 'Cricket Match')}")
            
            team1 = match.get("team1", {}).get("name", "Team 1")
            team2 = match.get("team2", {}).get("name", "Team 2")
            score1 = match.get("team1", {}).get("score", "-")
            score2 = match.get("team2", {}).get("score", "-")
            
            st.markdown(f"**{team1}** {score1} vs **{team2}** {score2}")
            st.caption(f"📍 {match.get('venue', 'Unknown Venue')}")
        
        # Match date
        with col3:
            match_date = match.get("match_date", "TBD")
            st.caption(f"📅 {match_date}")
        
        st.divider()


def display_no_matches():
    """Display message when no matches available."""
    st.info("🏏 No live matches at the moment. Check back later for upcoming matches!")


def display_filter_options():
    """Display filter options for matches."""
    st.markdown("### 🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        match_type = st.multiselect(
            "Match Type",
            ["Test", "ODI", "T20", "T20I", "All"],
            default=["All"]
        )
    
    with col2:
        status = st.multiselect(
            "Status",
            ["Live", "Upcoming", "Completed"],
            default=["Live"]
        )
    
    with col3:
        format_type = st.multiselect(
            "Format",
            ["International", "Domestic", "League"],
            default=["International"]
        )
    
    return match_type, status, format_type


def filter_matches(matches, match_type, status, format_type):
    """
    Filter matches based on selected criteria.
    
    Args:
        matches (list): List of all matches.
        match_type (list): Desired match types.
        status (list): Desired statuses.
        format_type (list): Desired formats.
        
    Returns:
        list: Filtered matches.
    """
    filtered = matches
    
    # Filter by type
    if match_type and "All" not in match_type:
        filtered = [m for m in filtered if m.get("type") in match_type]
    
    # Filter by status
    if status:
        filtered = [m for m in filtered if any(s in m.get("status", "").upper() for s in status)]
    
    # Filter by format
    if format_type:
        filtered = [m for m in filtered if m.get("format") in format_type]
    
    return filtered


def display_match_statistics():
    """Display overall match statistics."""
    st.markdown("### 📊 Match Statistics")
    
    matches = fetch_matches()
    
    if matches:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            live_count = len([m for m in matches if "LIVE" in m.get("status", "").upper()])
            st.metric("Live Matches", live_count)
        
        with col2:
            upcoming_count = len([m for m in matches if "UPCOMING" in m.get("status", "").upper()])
            st.metric("Upcoming", upcoming_count)
        
        with col3:
            completed_count = len([m for m in matches if "COMPLETED" in m.get("status", "").upper()])
            st.metric("Completed", completed_count)
        
        with col4:
            total_count = len(matches)
            st.metric("Total Matches", total_count)
    else:
        st.warning("Unable to fetch match statistics")


def display_live_matches():
    """
    Fetch and display ongoing matches in real-time.
    """
    display_header()
    
    # Refresh button
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("")  # Spacing
    
    # Display statistics
    display_match_statistics()
    st.markdown("---")
    
    # Filter options
    display_filter_options()
    st.markdown("---")
    
    # Fetch and display matches
    try:
        matches = fetch_matches()
        
        if matches:
            st.markdown(f"### Found {len(matches)} matches")
            
            for match in matches:
                display_match_card(match)
        else:
            display_no_matches()
            
    except Exception as e:
        st.error(f"Error loading matches: {str(e)}")
        logger.error(f"Error loading matches: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.caption("✓ Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def display_scorecard(match_id):
    """
    Display detailed scorecard for a specific match.
    
    Args:
        match_id (str): Match ID to retrieve scorecard.
    """
    st.markdown(f"## Match Scorecard - {match_id}")
    
    try:
        scorecard = api_handler.fetch_match_scorecard(match_id)
        
        if scorecard:
            # Display scorecard data
            st.json(scorecard)
        else:
            st.warning("Scorecard not available")
            
    except Exception as e:
        st.error(f"Error loading scorecard: {str(e)}")


def display_player_info(player_id):
    """
    Display player information and current form.
    
    Args:
        player_id (str): Player ID.
    """
    st.markdown(f"## Player Info - {player_id}")
    st.info("Player information will be displayed here")


if __name__ == "__main__":
    display_live_matches()
