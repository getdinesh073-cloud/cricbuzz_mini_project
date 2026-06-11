"""
CRUD Operations Page

Full Create, Read, Update, Delete operations on player and match data.
Form-based UI for data manipulation.
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime

from utils import db_connection

logger = logging.getLogger(__name__)


def display_header():
    """Display page header."""
    st.markdown("# 🛠️ CRUD Operations")
    st.markdown("Create, Read, Update, and Delete cricket data")
    st.markdown("---")


def create_player_form():
    """Display form to add a new player record."""
    st.markdown("## ➕ Create Player")
    
    with st.form("create_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            player_id = st.number_input("Player ID", min_value=1, step=1)
            full_name = st.text_input("Full Name")
            country = st.selectbox("Country", ["India", "Australia", "England", "Pakistan", "New Zealand", "South Africa", "West Indies", "Sri Lanka", "Bangladesh"])
        
        with col2:
            playing_role = st.selectbox("Playing Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            batting_style = st.selectbox("Batting Style", ["Right-handed", "Left-handed"])
            bowling_style = st.selectbox("Bowling Style", ["Right-arm Fast", "Right-arm Medium", "Left-arm Fast", "Left-arm Medium", "Right-arm Leg Spinner", "Right-arm Off Spinner", "Left-arm Chinaman"])
        
        dob = st.date_input("Date of Birth", value=datetime(2000, 1, 1))
        
        submitted = st.form_submit_button("Create Player", use_container_width=True)
        
        if submitted:
            if full_name and country:
                try:
                    # SQL query to insert player
                    query = """
                        INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style, date_of_birth)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    params = (player_id, full_name, country, playing_role, batting_style, bowling_style, dob)
                    
                    db_connection.execute_query(query, params=params, fetch="none")
                    st.success(f"✓ Player '{full_name}' created successfully!")
                    logger.info(f"Player created: {full_name}")
                    
                except Exception as e:
                    st.error(f"✗ Error creating player: {str(e)}")
                    logger.error(f"Error creating player: {str(e)}")
            else:
                st.warning("Please fill in required fields (Name, Country)")


def read_player_data():
    """Fetch and display existing player records."""
    st.markdown("## 📖 Read Players")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_type = st.radio("Search by:", ["All Players", "Country", "Playing Role"], key="read_player_type")
    
    with col2:
        if search_type == "Country":
            country_filter = st.text_input("Enter country name")
        elif search_type == "Playing Role":
            role_filter = st.selectbox("Select role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        else:
            country_filter = None
            role_filter = None
    
    try:
        if search_type == "All Players":
            query = "SELECT * FROM players LIMIT 100"
        elif search_type == "Country":
            query = "SELECT * FROM players WHERE country = ?"
            results = db_connection.execute_query(query, params=(country_filter,), fetch="all")
        else:
            query = "SELECT * FROM players WHERE playing_role = ?"
            results = db_connection.execute_query(query, params=(role_filter,), fetch="all")
        
        results = db_connection.execute_query(query, params=None, fetch="all")
        
        if results:
            df = pd.DataFrame(results, columns=["Player_ID", "Full_Name", "Country", "Role", "Batting_Style", "Bowling_Style", "DOB"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"✓ Retrieved {len(results)} player records")
        else:
            st.info("No players found")
            
    except Exception as e:
        st.error(f"✗ Error reading players: {str(e)}")
        logger.error(f"Error reading players: {str(e)}")


def update_player_form():
    """Display form to update player information."""
    st.markdown("## ✏️ Update Player")
    
    col1, col2 = st.columns(2)
    
    with col1:
        player_id = st.number_input("Player ID to Update", min_value=1, step=1, key="update_pid")
    
    with col2:
        if st.button("Load Player Data", key="load_player"):
            st.session_state.load_player = True
    
    if st.session_state.get("load_player"):
        try:
            query = "SELECT * FROM players WHERE player_id = ?"
            result = db_connection.execute_query(query, params=(player_id,), fetch="one")
            
            if result:
                with st.form("update_player_form"):
                    full_name = st.text_input("Full Name", value=result[1] if len(result) > 1 else "")
                    country = st.text_input("Country", value=result[2] if len(result) > 2 else "")
                    playing_role = st.text_input("Playing Role", value=result[3] if len(result) > 3 else "")
                    
                    submitted = st.form_submit_button("Update Player")
                    
                    if submitted:
                        update_query = "UPDATE players SET full_name=?, country=?, playing_role=? WHERE player_id=?"
                        db_connection.execute_query(update_query, params=(full_name, country, playing_role, player_id), fetch="none")
                        st.success(f"✓ Player {player_id} updated successfully!")
                        logger.info(f"Player {player_id} updated")
            else:
                st.warning(f"Player ID {player_id} not found")
                
        except Exception as e:
            st.error(f"✗ Error loading player: {str(e)}")


def delete_player_record():
    """Display interface to delete player records."""
    st.markdown("## 🗑️ Delete Player")
    
    player_id = st.number_input("Player ID to Delete", min_value=1, step=1, key="delete_pid")
    
    if st.button("Delete Player", use_container_width=True, type="secondary"):
        if st.confirm("Are you sure? This action cannot be undone."):
            try:
                query = "DELETE FROM players WHERE player_id = ?"
                db_connection.execute_query(query, params=(player_id,), fetch="none")
                st.success(f"✓ Player {player_id} deleted successfully!")
                logger.info(f"Player {player_id} deleted")
            except Exception as e:
                st.error(f"✗ Error deleting player: {str(e)}")


def create_match_form():
    """Display form to add a new match record."""
    st.markdown("## ➕ Create Match")
    
    with st.form("create_match_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            match_id = st.number_input("Match ID", min_value=1, step=1, key="match_id_new")
            description = st.text_input("Match Description")
            match_date = st.date_input("Match Date")
            match_type = st.selectbox("Match Type", ["Test", "ODI", "T20", "T20I"], key="match_type_new")
        
        with col2:
            team1_id = st.number_input("Team 1 ID", min_value=1, step=1, key="team1_new")
            team2_id = st.number_input("Team 2 ID", min_value=1, step=1, key="team2_new")
            venue_id = st.number_input("Venue ID", min_value=1, step=1, key="venue_new")
            status = st.selectbox("Status", ["Scheduled", "Live", "Completed"], key="status_new")
        
        submitted = st.form_submit_button("Create Match", use_container_width=True)
        
        if submitted:
            if description and match_date:
                try:
                    query = """
                        INSERT INTO matches (match_id, description, team1_id, team2_id, venue_id, match_date, match_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                    params = (match_id, description, team1_id, team2_id, venue_id, match_date, match_type)
                    db_connection.execute_query(query, params=params, fetch="none")
                    st.success(f"✓ Match '{description}' created successfully!")
                    logger.info(f"Match created: {description}")
                except Exception as e:
                    st.error(f"✗ Error creating match: {str(e)}")
            else:
                st.warning("Please fill in required fields")


def read_match_data():
    """Fetch and display existing match records."""
    st.markdown("## 📖 Read Matches")
    
    search_type = st.radio("Search by:", ["All Matches", "Date Range", "Status"], key="read_match_type")
    
    try:
        if search_type == "All Matches":
            query = "SELECT * FROM matches LIMIT 50"
            results = db_connection.execute_query(query, fetch="all")
        elif search_type == "Date Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date")
            with col2:
                end_date = st.date_input("End Date")
            query = "SELECT * FROM matches WHERE match_date BETWEEN ? AND ?"
            results = db_connection.execute_query(query, params=(start_date, end_date), fetch="all")
        else:
            status = st.selectbox("Match Status", ["Scheduled", "Live", "Completed"])
            query = "SELECT * FROM matches LIMIT 50"
            results = db_connection.execute_query(query, fetch="all")
        
        if results:
            df = pd.DataFrame(results, columns=["Match_ID", "Description", "Team1_ID", "Team2_ID", "Venue_ID", "Match_Date", "Type", "Winner_ID", "Margin", "Margin_Type", "Toss_Winner", "Toss_Decision"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success(f"✓ Retrieved {len(results)} match records")
        else:
            st.info("No matches found")
            
    except Exception as e:
        st.error(f"✗ Error reading matches: {str(e)}")


def update_match_form():
    """Display form to update match information."""
    st.markdown("## ✏️ Update Match")
    st.info("Match update functionality - select match and update details")


def delete_match_record():
    """Display interface to delete match records."""
    st.markdown("## 🗑️ Delete Match")
    st.info("Match deletion functionality - enter match ID and confirm deletion")


def crud_home():
    """Render CRUD operations main interface."""
    display_header()
    
    # Create tabs for different CRUD operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Players - Create", "Players - Read", "Players - Update", "Matches - Create", "Matches - Read"])
    
    with tab1:
        create_player_form()
    
    with tab2:
        read_player_data()
    
    with tab3:
        update_player_form()
    
    with tab4:
        create_match_form()
    
    with tab5:
        read_match_data()
    
    st.markdown("---")
    st.info(
        """
        **CRUD Operations Guide:**
        - **Create**: Add new player or match records
        - **Read**: View existing records with filters
        - **Update**: Modify existing player details
        - **Delete**: Remove records (use with caution)
        """
    )


if __name__ == "__main__":
    crud_home()
