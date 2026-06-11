"""
Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

Main entry point for the Streamlit application.
Multi-page app for cricket analytics, live matches, player stats, and CRUD operations.
"""

import streamlit as st
import logging
from pathlib import Path

import config
from utils import db_connection, api_handler

# Configure page settings
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded",
)

# Configure logging
logging.basicConfig(
    level=config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

# Custom CSS
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        background-color: #f0f2f6;
    }
    .main-header {
        color: #1f77b4;
        text-align: center;
        font-size: 2.5em;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_session_state():
    """
    Initialize Streamlit session state variables.
    """
    if "db_connected" not in st.session_state:
        st.session_state.db_connected = False
    if "api_available" not in st.session_state:
        st.session_state.api_available = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "cache_data" not in st.session_state:
        st.session_state.cache_data = {}


def check_system_status():
    """
    Check database and API connectivity status.
    Returns status information.
    """
    status = {
        "database": False,
        "api": False,
        "messages": []
    }
    
    # Check database
    try:
        conn = db_connection.get_db_connection()
        status["database"] = conn is not None
        status["messages"].append(
            f"✓ Database ({config.DB_TYPE.upper()}): Connected"
        )
    except Exception as e:
        status["messages"].append(f"✗ Database: {str(e)}")
    
    # Check API
    try:
        api_status = api_handler.test_api_connection()
        status["api"] = api_status
        if api_status:
            status["messages"].append("✓ Cricbuzz API: Connected")
        else:
            status["messages"].append("✗ Cricbuzz API: Not responding")
    except Exception as e:
        status["messages"].append(f"✗ API Error: {str(e)}")
    
    return status


def render_sidebar():
    """
    Render application sidebar with navigation and status.
    """
    with st.sidebar:
        st.markdown("### 🏏 Navigation")
        
        # Status section
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        status = check_system_status()
        
        col1, col2 = st.columns(2)
        with col1:
            db_status = "🟢 Online" if status["database"] else "🔴 Offline"
            st.metric("Database", db_status)
        with col2:
            api_status = "🟢 Online" if status["api"] else "🔴 Offline"
            st.metric("API", api_status)
        
        # Status messages
        for msg in status["messages"]:
            if "✓" in msg:
                st.success(msg)
            else:
                st.error(msg)
        
        # About section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.info(
            "**Cricbuzz LiveStats** v1.0\n\n"
            "Real-time cricket analytics with SQL-based insights.\n\n"
            f"Database: {config.DB_TYPE.upper()}\n"
            f"API: {config.CRICBUZZ_API_BASE_URL}"
        )


def render_home_page():
    """
    Render the home page with project overview.
    """
    st.markdown(
        '<p class="main-header">🏏 Cricbuzz LiveStats</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color: #666;'>"
        "Real-Time Cricket Insights & SQL-Based Analytics"
        "</p>",
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Welcome section
    st.markdown("## 👋 Welcome!")
    st.write(
        """
        This is a comprehensive cricket analytics dashboard that integrates 
        live data from the Cricbuzz API with a SQL database to create an 
        interactive web application.
        """
    )
    
    # Features section
    st.markdown("## ✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⚡ Live Matches")
        st.write("Real-time cricket matches with live scorecards and player info")
        
        st.markdown("### 📊 Player Stats")
        st.write("Top batting and bowling statistics with filtering options")
    
    with col2:
        st.markdown("### 🔍 SQL Analytics")
        st.write("25+ SQL queries for cricket insights and analysis")
        
        st.markdown("### 🛠️ CRUD Operations")
        st.write("Manage player and match data with form-based UI")
    
    # Quick stats section
    st.markdown("## 📈 Quick Stats")
    
    try:
        if status_info["database"]:
            col1, col2, col3 = st.columns(3)
            
            # Count tables
            with col1:
                st.metric("Database Type", config.DB_TYPE.upper())
            with col2:
                st.metric("Database Name", config.DB_NAME)
            with col3:
                st.metric("API Timeout (s)", config.API_TIMEOUT)
    except:
        pass
    
    # Getting started
    st.markdown("## 🚀 Getting Started")
    
    with st.expander("📖 Setup Instructions", expanded=False):
        st.markdown(
            """
            1. **Database Setup**: Configure your database connection in `config.py`
            2. **API Key**: Add your Cricbuzz API key to environment variables
            3. **Installation**: Install requirements with `pip install -r requirements.txt`
            4. **Run App**: Start with `streamlit run main.py`
            5. **Explore**: Navigate through pages using the sidebar
            """
        )
    
    with st.expander("🔗 Useful Links", expanded=False):
        st.markdown(
            """
            - [Cricbuzz Website](https://www.cricbuzz.com)
            - [Streamlit Docs](https://docs.streamlit.io)
            - [Python SQL](https://www.python.org)
            - [Project README](./README.md)
            """
        )


def main():
    """
    Main function to run the Streamlit application.
    """
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Get system status for use in home page
    global status_info
    status_info = check_system_status()
    
    # Main content
    render_home_page()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <p style='text-align: center; color: #999; font-size: 0.8em;'>
        © 2026 Cricbuzz LiveStats | Built with Streamlit & Python
        </p>
        """,
        unsafe_allow_html=True
    )
    
    logger.info("App loaded successfully")


if __name__ == "__main__":
    main()
