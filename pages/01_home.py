"""
Home Page

Project overview and navigation hub for Cricbuzz LiveStats.
Displays project description, features, and instructions.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def display_header():
    """Display page header with title and description."""
    st.markdown("# 🏠 Home")
    st.markdown("---")
    st.markdown(
        """
        Welcome to **Cricbuzz LiveStats** - Your comprehensive cricket analytics platform!
        
        This application integrates real-time cricket data from the Cricbuzz API 
        with a powerful SQL database to deliver unparalleled cricket insights and analytics.
        """
    )


def display_features():
    """Display main application features."""
    st.markdown("## ✨ Features Overview")
    
    features = {
        "⚡ Live Matches": {
            "icon": "📺",
            "description": "Real-time cricket matches with detailed scorecards, player information, and venue details",
            "link": "02_live_matches"
        },
        "📊 Player Stats": {
            "icon": "🏏",
            "description": "Top batting and bowling statistics with format filtering and player comparisons",
            "link": "03_player_stats"
        },
        "🔍 SQL Analytics": {
            "icon": "📈",
            "description": "25+ SQL queries for advanced cricket insights (beginner to expert level)",
            "link": "04_sql_analytics"
        },
        "🛠️ CRUD Operations": {
            "icon": "⚙️",
            "description": "Create, Read, Update, and Delete player and match records with form-based UI",
            "link": "05_crud_operations"
        },
    }
    
    cols = st.columns(2)
    for idx, (title, details) in enumerate(features.items()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f"### {details['icon']} {title}")
                st.write(details['description'])
                if st.button(f"Go to {title.split()[1]}", key=f"btn_{idx}"):
                    st.switch_page(f"pages/{details['link']}.py")


def display_use_cases():
    """Display business use cases."""
    st.markdown("## 💼 Use Cases")
    
    use_cases = [
        {
            "title": "📺 Sports Media & Broadcasting",
            "items": [
                "Real-time match updates for commentary teams",
                "Player performance analysis for pre-match discussions",
                "Historical data trends for match predictions"
            ]
        },
        {
            "title": "🎮 Fantasy Cricket Platforms",
            "items": [
                "Player form analysis and recent performance tracking",
                "Head-to-head statistics for team selection",
                "Real-time score updates for fantasy leagues"
            ]
        },
        {
            "title": "📈 Cricket Analytics Firms",
            "items": [
                "Advanced statistical modeling and player evaluation",
                "Performance trend analysis across formats",
                "Data-driven insights for team management"
            ]
        },
        {
            "title": "🎓 Educational Institutions",
            "items": [
                "Teaching database operations with real-world data",
                "SQL practice with engaging cricket datasets",
                "API integration and web development learning"
            ]
        },
    ]
    
    for uc in use_cases:
        with st.expander(uc["title"]):
            for item in uc["items"]:
                st.write(f"• {item}")


def display_tech_stack():
    """Display technology stack."""
    st.markdown("## 🛠️ Technology Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Frontend")
        st.markdown(
            """
            - **Streamlit** - Web framework
            - **Pandas** - Data manipulation
            - **Plotly** - Visualizations
            """
        )
    
    with col2:
        st.markdown("### Backend")
        st.markdown(
            """
            - **Python** - Core language
            - **Requests** - API calls
            - **SQLAlchemy** - ORM
            """
        )
    
    with col3:
        st.markdown("### Database")
        st.markdown(
            """
            - **SQLite** - Local development
            - **PostgreSQL** - Production
            - **MySQL** - Alternative
            """
        )


def display_getting_started():
    """Display getting started section."""
    st.markdown("## 🚀 Getting Started")
    
    with st.container():
        st.markdown("### Quick Start Steps")
        
        steps = [
            ("1️⃣", "**Clone Repository**", "Get the latest code from GitHub"),
            ("2️⃣", "**Install Dependencies**", "Run `pip install -r requirements.txt`"),
            ("3️⃣", "**Setup Database**", "Configure your database in `.env` or `config.py`"),
            ("4️⃣", "**Configure API**", "Add Cricbuzz API key to environment variables"),
            ("5️⃣", "**Run Application**", "Execute `streamlit run main.py`"),
            ("6️⃣", "**Explore Features**", "Navigate through different pages using sidebar"),
        ]
        
        for step_num, step_title, step_desc in steps:
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                st.markdown(f"### {step_num}")
            with col2:
                st.markdown(f"**{step_title}**")
                st.caption(step_desc)


def display_documentation_links():
    """Display links to documentation."""
    st.markdown("## 📚 Documentation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📖 Full README", use_container_width=True):
            st.info("See README.md in the project root for complete documentation")
        
        if st.button("⚙️ Setup Guide", use_container_width=True):
            st.info("Check docs/SETUP.md for detailed setup instructions")
    
    with col2:
        if st.button("🔗 API Reference", use_container_width=True):
            st.info("See docs/API_REFERENCE.md for API integration details")
        
        if st.button("🚀 Deployment Guide", use_container_width=True):
            st.info("Check docs/DEPLOYMENT.md for production deployment options")


def display_quick_stats():
    """Display quick statistics."""
    st.markdown("## 📊 Quick Facts")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("SQL Queries", "25+", "Beginner to Advanced")
    
    with col2:
        st.metric("Database Support", "3", "SQLite, PostgreSQL, MySQL")
    
    with col3:
        st.metric("API Endpoints", "6+", "Live data feeds")
    
    with col4:
        st.metric("Pages", "5", "Full dashboard")


def display_footer():
    """Display page footer."""
    st.markdown("---")
    st.markdown(
        """
        <p style='text-align: center; color: #999; font-size: 0.85em;'>
        🏏 Cricbuzz LiveStats v1.0 | Built with Streamlit & Python | Last Updated: June 2026
        </p>
        """,
        unsafe_allow_html=True
    )


def home_page():
    """
    Render the complete home page with all sections.
    """
    display_header()
    display_features()
    
    st.markdown("---")
    display_use_cases()
    
    st.markdown("---")
    display_tech_stack()
    
    st.markdown("---")
    display_getting_started()
    
    st.markdown("---")
    display_documentation_links()
    
    st.markdown("---")
    display_quick_stats()
    
    display_footer()
    
    logger.info("Home page rendered successfully")


if __name__ == "__main__":
    home_page()
