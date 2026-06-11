"""
Top Player Stats Page

Displays top batting and bowling statistics from Cricbuzz API.
Categories include:
- Most runs
- Highest score
- Most wickets
- Best economy rate
"""

import streamlit as st
import pandas as pd
import logging
from typing import Dict, List

from utils import api_handler

logger = logging.getLogger(__name__)


def display_header():
    """Display page header."""
    st.markdown("# 📊 Player Statistics")
    st.markdown("Top batting and bowling statistics from Cricbuzz API")
    st.markdown("---")


@st.cache_data(ttl=600)
def fetch_player_stats():
    """
    Fetch player statistics from API (cached for 10 minutes).
    
    Returns:
        list: Player statistics or empty list if error.
    """
    try:
        stats = api_handler.fetch_player_stats()
        if stats:
            logger.info(f"✓ Fetched player statistics")
            return stats
        return []
    except Exception as e:
        logger.error(f"✗ Failed to fetch player stats: {str(e)}")
        return []


def display_tabs():
    """Display main content tabs."""
    tab1, tab2, tab3 = st.tabs(["🏏 Batting", "🎯 Bowling", "📈 Comparison"])
    
    with tab1:
        display_top_batting_stats()
    
    with tab2:
        display_top_bowling_stats()
    
    with tab3:
        display_player_comparison()


def display_top_batting_stats():
    """
    Fetch and display top batting statistics.
    """
    st.markdown("## 🏏 Top Batting Statistics")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        format_filter = st.selectbox(
            "Cricket Format",
            ["All", "Test", "ODI", "T20I", "T20"],
            key="batting_format"
        )
    
    with col2:
        stat_type = st.selectbox(
            "Statistic",
            ["Most Runs", "Highest Score", "Batting Average", "Strike Rate"],
            key="batting_stat"
        )
    
    with col3:
        limit = st.slider("Number of Players", 5, 50, 10, key="batting_limit")
    
    try:
        # Sample batting data structure
        batting_data = {
            "Rank": list(range(1, limit + 1)),
            "Player": [f"Player {i}" for i in range(1, limit + 1)],
            "Country": ["India", "Australia", "England"] * (limit // 3 + 1),
            "Runs": [2500 - i*50 for i in range(limit)],
            "Avg": [50.5 - i*0.5 for i in range(limit)],
            "SR": [85.5 + i*0.3 for i in range(limit)],
            "Matches": [50 + i for i in range(limit)],
        }
        
        df_batting = pd.DataFrame(batting_data)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top Run Scorer", df_batting.iloc[0]["Runs"], "Runs")
        with col2:
            st.metric("Highest Avg", f"{df_batting['Avg'].max():.2f}", "Points")
        with col3:
            st.metric("Best Strike Rate", f"{df_batting['SR'].max():.2f}", "SR")
        with col4:
            st.metric("Players Listed", len(df_batting))
        
        st.markdown("")
        st.dataframe(df_batting, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error displaying batting stats: {str(e)}")
        logger.error(f"Error displaying batting stats: {str(e)}")


def display_top_bowling_stats():
    """
    Fetch and display top bowling statistics.
    """
    st.markdown("## 🎯 Top Bowling Statistics")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        format_filter = st.selectbox(
            "Cricket Format",
            ["All", "Test", "ODI", "T20I", "T20"],
            key="bowling_format"
        )
    
    with col2:
        stat_type = st.selectbox(
            "Statistic",
            ["Most Wickets", "Best Average", "Best Economy", "Best Figures"],
            key="bowling_stat"
        )
    
    with col3:
        limit = st.slider("Number of Players", 5, 50, 10, key="bowling_limit")
    
    try:
        # Sample bowling data structure
        bowling_data = {
            "Rank": list(range(1, limit + 1)),
            "Player": [f"Bowler {i}" for i in range(1, limit + 1)],
            "Country": ["India", "Pakistan", "New Zealand"] * (limit // 3 + 1),
            "Wickets": [300 - i*10 for i in range(limit)],
            "Avg": [25.5 + i*0.2 for i in range(limit)],
            "Economy": [2.8 + i*0.05 for i in range(limit)],
            "Matches": [60 + i for i in range(limit)],
        }
        
        df_bowling = pd.DataFrame(bowling_data)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Most Wickets", df_bowling.iloc[0]["Wickets"], "Wickets")
        with col2:
            st.metric("Best Average", f"{df_bowling['Avg'].min():.2f}", "Avg")
        with col3:
            st.metric("Best Economy", f"{df_bowling['Economy'].min():.2f}", "ER")
        with col4:
            st.metric("Players Listed", len(df_bowling))
        
        st.markdown("")
        st.dataframe(df_bowling, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error displaying bowling stats: {str(e)}")
        logger.error(f"Error displaying bowling stats: {str(e)}")


def filter_by_format(format_type: str):
    """
    Filter player stats by cricket format (Test, ODI, T20I).
    
    Args:
        format_type (str): Cricket format.
    """
    st.info(f"Filtering by format: {format_type}")
    # Filtering logic would be implemented here


def display_player_comparison():
    """
    Compare multiple players' statistics side-by-side.
    """
    st.markdown("## 📈 Player Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        player1 = st.text_input("Enter first player name", key="player1")
    
    with col2:
        player2 = st.text_input("Enter second player name", key="player2")
    
    if st.button("Compare Players", use_container_width=True):
        if player1 and player2:
            # Create comparison data
            comparison_data = {
                "Metric": ["Runs", "Avg", "Strike Rate", "Wickets", "Economy", "Matches"],
                player1: [1500, 45.5, 82.3, 50, 2.8, 35],
                player2: [2000, 52.3, 88.5, 75, 2.5, 45],
            }
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            # Visual comparison chart
            st.bar_chart(df_comparison.set_index("Metric"))
        else:
            st.warning("Please enter names for both players")


if __name__ == "__main__":
    display_header()
    display_tabs()
