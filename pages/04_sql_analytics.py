"""
SQL Queries & Analytics Page

Integrates 25+ advanced SQL queries on player and match database.
Covers beginner, intermediate, and advanced analytics use cases.

Beginner Level (Q1-Q8):
- Basic SELECT, WHERE, GROUP BY, ORDER BY

Intermediate Level (Q9-Q16):
- JOINs, subqueries, aggregate functions

Advanced Level (Q17-Q25):
- Window functions, CTEs, complex analytics
"""

import streamlit as st
import pandas as pd
import logging

from utils import db_connection

logger = logging.getLogger(__name__)


def display_header():
    """Display page header."""
    st.markdown("# 🔍 SQL Analytics & Queries")
    st.markdown("Execute 25+ SQL queries for cricket insights")
    st.markdown("---")


# ==================== BEGINNER QUERIES (Q1-Q8) ====================
BEGINNER_QUERIES = {
    "Q1: Players from India": {
        "description": "Find all players who represent India",
        "sql": """
            SELECT 
                full_name,
                playing_role,
                batting_style,
                bowling_style
            FROM players
            WHERE country = 'India'
            ORDER BY full_name
        """
    },
    "Q2: Recent Matches": {
        "description": "Show all cricket matches in the last 30 days",
        "sql": """
            SELECT 
                description,
                team1_id,
                team2_id,
                match_date,
                venue_id
            FROM matches
            WHERE match_date >= DATE('now', '-30 days')
            ORDER BY match_date DESC
        """
    },
    "Q3: Top 10 Run Scorers": {
        "description": "List top 10 highest run scorers in ODI cricket",
        "sql": """
            SELECT 
                p.full_name,
                SUM(ps.runs_scored) as total_runs,
                AVG(ps.batting_average) as batting_avg,
                COUNT(DISTINCT m.match_id) as matches
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE ps.format = 'ODI'
            GROUP BY p.player_id
            ORDER BY total_runs DESC
            LIMIT 10
        """
    },
    "Q4: Large Venues": {
        "description": "Display venues with capacity > 25,000",
        "sql": """
            SELECT 
                venue_name,
                city,
                country,
                capacity
            FROM venues
            WHERE capacity > 25000
            ORDER BY capacity DESC
        """
    },
    "Q5: Team Wins": {
        "description": "Calculate total wins for each team",
        "sql": """
            SELECT 
                team_name,
                COUNT(*) as total_wins
            FROM matches m
            JOIN teams t ON m.winning_team_id = t.team_id
            GROUP BY m.winning_team_id
            ORDER BY total_wins DESC
        """
    },
    "Q6: Players by Role": {
        "description": "Count players by playing role",
        "sql": """
            SELECT 
                playing_role,
                COUNT(*) as player_count
            FROM players
            WHERE playing_role IS NOT NULL
            GROUP BY playing_role
            ORDER BY player_count DESC
        """
    },
    "Q7: Highest Individual Score": {
        "description": "Find highest individual batting score in each format",
        "sql": """
            SELECT 
                format,
                MAX(runs_scored) as highest_score
            FROM performance_stats
            GROUP BY format
            ORDER BY highest_score DESC
        """
    },
    "Q8: Series in 2024": {
        "description": "Show all cricket series started in 2024",
        "sql": """
            SELECT 
                series_name,
                host_country,
                match_type,
                start_date,
                total_matches
            FROM series
            WHERE strftime('%Y', start_date) = '2024'
            ORDER BY start_date
        """
    }
}

# ==================== INTERMEDIATE QUERIES (Q9-Q16) ====================
INTERMEDIATE_QUERIES = {
    "Q9: All-rounder Performance": {
        "description": "Find all-rounders with 1000+ runs AND 50+ wickets",
        "sql": """
            SELECT 
                p.full_name,
                SUM(ps.runs_scored) as total_runs,
                SUM(ps.wickets_taken) as total_wickets,
                ps.format
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            WHERE p.playing_role = 'All-rounder'
            GROUP BY p.player_id, ps.format
            HAVING SUM(ps.runs_scored) > 1000 AND SUM(ps.wickets_taken) > 50
            ORDER BY total_runs DESC
        """
    },
    "Q10: Last 20 Completed Matches": {
        "description": "Get details of last 20 completed matches",
        "sql": """
            SELECT 
                description,
                team1_id,
                team2_id,
                winning_team_id,
                victory_margin,
                victory_type,
                venue_id,
                match_date
            FROM matches
            WHERE winning_team_id IS NOT NULL
            ORDER BY match_date DESC
            LIMIT 20
        """
    },
    "Q11: Multi-format Comparison": {
        "description": "Compare players' performance across formats",
        "sql": """
            SELECT 
                p.full_name,
                ps.format,
                SUM(ps.runs_scored) as runs,
                AVG(ps.batting_average) as avg_batting,
                AVG(ps.strike_rate) as avg_sr
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            GROUP BY p.player_id, ps.format
            HAVING COUNT(DISTINCT ps.format) >= 2
            ORDER BY p.full_name, ps.format
        """
    },
    "Q12: Home vs Away Performance": {
        "description": "Analyze team performance at home vs away",
        "sql": """
            SELECT 
                t.team_name,
                CASE WHEN v.country = t.country THEN 'Home' ELSE 'Away' END as venue_type,
                COUNT(m.match_id) as matches_played,
                SUM(CASE WHEN m.winning_team_id = t.team_id THEN 1 ELSE 0 END) as wins
            FROM teams t
            JOIN matches m ON (m.team1_id = t.team_id OR m.team2_id = t.team_id)
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY t.team_id, venue_type
            ORDER BY t.team_name, venue_type
        """
    },
    "Q13: Batting Partnerships": {
        "description": "Identify batting partnerships with 100+ combined runs",
        "sql": """
            SELECT 
                i1.player_id as player1,
                i2.player_id as player2,
                i1.runs + i2.runs as partnership_runs,
                i1.innings_id
            FROM innings i1
            JOIN innings i2 ON i1.innings_id = i2.innings_id 
                AND ABS(i1.batting_position - i2.batting_position) = 1
            WHERE i1.runs + i2.runs >= 100
            ORDER BY partnership_runs DESC
        """
    },
    "Q14: Bowling at Venues": {
        "description": "Examine bowling performance at specific venues",
        "sql": """
            SELECT 
                p.full_name,
                v.venue_name,
                COUNT(DISTINCT bp.bowling_id) as matches_played,
                SUM(bp.wickets) as total_wickets,
                AVG(bp.economy_rate) as avg_economy
            FROM players p
            JOIN bowling_performance bp ON p.player_id = bp.bowler_id
            JOIN matches m ON bp.match_id = m.match_id
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY p.player_id, v.venue_id
            HAVING COUNT(DISTINCT bp.bowling_id) >= 3
            ORDER BY avg_economy
        """
    },
    "Q15: Close Match Performance": {
        "description": "Players performing well in close matches",
        "sql": """
            SELECT 
                p.full_name,
                COUNT(DISTINCT m.match_id) as close_matches,
                AVG(ps.runs_scored) as avg_runs,
                SUM(CASE WHEN m.winning_team_id = ps.match_id THEN 1 ELSE 0 END) as wins_when_batting
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE ABS(m.victory_margin) < 50 OR ABS(m.victory_margin) < 5
            GROUP BY p.player_id
            ORDER BY avg_runs DESC
        """
    },
    "Q16: Yearly Performance Trends": {
        "description": "Track player performance trends yearly since 2020",
        "sql": """
            SELECT 
                p.full_name,
                strftime('%Y', m.match_date) as year,
                AVG(ps.runs_scored) as avg_runs,
                AVG(ps.strike_rate) as avg_sr,
                COUNT(DISTINCT m.match_id) as matches
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE strftime('%Y', m.match_date) >= '2020'
            GROUP BY p.player_id, year
            HAVING COUNT(DISTINCT m.match_id) >= 5
            ORDER BY p.full_name, year DESC
        """
    }
}

# ==================== ADVANCED QUERIES (Q17-Q25) ====================
ADVANCED_QUERIES = {
    "Q17: Toss Advantage Analysis": {
        "description": "Investigate toss advantage in match outcomes",
        "sql": """
            SELECT 
                toss_decision,
                COUNT(*) as total_matches,
                SUM(CASE WHEN winning_team_id = toss_winner_id THEN 1 ELSE 0 END) as wins_by_toss_winner,
                ROUND(100.0 * SUM(CASE WHEN winning_team_id = toss_winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) as win_percentage
            FROM matches
            WHERE toss_winner_id IS NOT NULL
            GROUP BY toss_decision
            ORDER BY win_percentage DESC
        """
    },
    "Q18: Economical Bowlers": {
        "description": "Most economical bowlers in limited-overs cricket",
        "sql": """
            SELECT 
                p.full_name,
                COUNT(DISTINCT bp.bowling_id) as matches,
                SUM(bp.wickets) as wickets,
                AVG(bp.economy_rate) as avg_economy
            FROM players p
            JOIN bowling_performance bp ON p.player_id = bp.bowler_id
            JOIN matches m ON bp.match_id = m.match_id
            JOIN performance_stats ps ON p.player_id = ps.player_id AND m.match_id = ps.match_id
            WHERE ps.format IN ('ODI', 'T20')
            GROUP BY p.player_id
            HAVING COUNT(DISTINCT bp.bowling_id) >= 10 AND AVG(bp.overs_bowled) >= 2
            ORDER BY avg_economy
            LIMIT 20
        """
    },
    "Q19: Consistent Batsmen": {
        "description": "Most consistent batsmen based on std deviation of runs",
        "sql": """
            SELECT 
                p.full_name,
                AVG(ps.runs_scored) as avg_runs,
                ROUND(sqrt(sum((ps.runs_scored - avg(ps.runs_scored)) * (ps.runs_scored - avg(ps.runs_scored))) / count(*)), 2) as std_dev,
                COUNT(*) as innings
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            WHERE ps.runs_scored IS NOT NULL AND strftime('%Y', NOW()) - 2 >= strftime('%Y', (SELECT min(match_date) FROM matches))
            GROUP BY p.player_id
            HAVING COUNT(*) >= 10 AND avg(ps.runs_scored) > 20
            ORDER BY std_dev
            LIMIT 20
        """
    },
    "Q20: Multi-format Players": {
        "description": "Players across formats with 20+ total matches",
        "sql": """
            SELECT 
                p.full_name,
                SUM(CASE WHEN ps.format = 'Test' THEN 1 ELSE 0 END) as test_matches,
                SUM(CASE WHEN ps.format = 'ODI' THEN 1 ELSE 0 END) as odi_matches,
                SUM(CASE WHEN ps.format = 'T20' THEN 1 ELSE 0 END) as t20_matches,
                AVG(CASE WHEN ps.format = 'Test' THEN ps.batting_average END) as test_avg,
                AVG(CASE WHEN ps.format = 'ODI' THEN ps.batting_average END) as odi_avg,
                AVG(CASE WHEN ps.format = 'T20' THEN ps.batting_average END) as t20_avg
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            GROUP BY p.player_id
            HAVING COUNT(DISTINCT ps.format) >= 2 AND COUNT(*) >= 20
            ORDER BY COUNT(*) DESC
        """
    },
    "Q21: Player Performance Ranking": {
        "description": "Comprehensive ranking combining batting, bowling, fielding",
        "sql": """
            SELECT 
                p.full_name,
                ROUND((SUM(ps.runs_scored) * 0.01) + (AVG(ps.batting_average) * 0.5) + (AVG(ps.strike_rate) * 0.3) +
                      (SUM(ps.wickets_taken) * 2) + ((50 - AVG(ps.bowling_average)) * 0.5) + ((6 - AVG(ps.economy_rate)) * 2), 2) as performance_score,
                ps.format
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            GROUP BY p.player_id, ps.format
            ORDER BY performance_score DESC
            LIMIT 30
        """
    },
    "Q22: Head-to-Head Analysis": {
        "description": "Head-to-head match analysis between teams",
        "sql": """
            SELECT 
                t1.team_name as team1,
                t2.team_name as team2,
                COUNT(*) as total_matches,
                SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) as t1_wins,
                SUM(CASE WHEN m.winning_team_id = t2.team_id THEN 1 ELSE 0 END) as t2_wins,
                ROUND(100.0 * SUM(CASE WHEN m.winning_team_id = t1.team_id THEN 1 ELSE 0 END) / COUNT(*), 2) as t1_win_pct
            FROM teams t1
            JOIN teams t2 ON t1.team_id < t2.team_id
            JOIN matches m ON (m.team1_id = t1.team_id AND m.team2_id = t2.team_id) 
                           OR (m.team1_id = t2.team_id AND m.team2_id = t1.team_id)
            WHERE m.match_date >= DATE('now', '-3 years')
            GROUP BY t1.team_id, t2.team_id
            HAVING COUNT(*) >= 5
            ORDER BY total_matches DESC
        """
    },
    "Q23: Player Form Analysis": {
        "description": "Recent player form and momentum tracking",
        "sql": """
            SELECT 
                p.full_name,
                AVG(CASE WHEN rank <= 5 THEN ps.runs_scored END) as recent_5_avg,
                AVG(CASE WHEN rank <= 10 THEN ps.runs_scored END) as recent_10_avg,
                CASE 
                    WHEN AVG(CASE WHEN rank <= 5 THEN ps.runs_scored END) > AVG(CASE WHEN rank <= 10 THEN ps.runs_scored END) THEN 'Improving'
                    WHEN AVG(CASE WHEN rank <= 5 THEN ps.runs_scored END) < AVG(CASE WHEN rank <= 10 THEN ps.runs_scored END) * 0.9 THEN 'Declining'
                    ELSE 'Stable'
                END as form_status
            FROM players p
            JOIN (SELECT *, ROW_NUMBER() OVER (PARTITION BY player_id ORDER BY match_id DESC) as rank FROM performance_stats) ps 
                ON p.player_id = ps.player_id
            WHERE ps.runs_scored IS NOT NULL
            GROUP BY p.player_id
            ORDER BY recent_5_avg DESC
            LIMIT 20
        """
    },
    "Q24: Batting Partnerships Success": {
        "description": "Most successful batting partnerships",
        "sql": """
            SELECT 
                p1.full_name as player1,
                p2.full_name as player2,
                COUNT(*) as partnerships,
                AVG(i1.runs + i2.runs) as avg_partnership_runs,
                SUM(CASE WHEN i1.runs + i2.runs > 50 THEN 1 ELSE 0 END) as partnerships_50_plus,
                MAX(i1.runs + i2.runs) as highest_partnership,
                ROUND(100.0 * SUM(CASE WHEN i1.runs + i2.runs > 50 THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
            FROM players p1
            JOIN players p2 ON p1.player_id < p2.player_id
            JOIN innings i1 ON p1.player_id = i1.player_id
            JOIN innings i2 ON p2.player_id = i2.player_id AND i1.innings_id = i2.innings_id
            WHERE ABS(i1.batting_position - i2.batting_position) = 1
            GROUP BY p1.player_id, p2.player_id
            HAVING COUNT(*) >= 5
            ORDER BY avg_partnership_runs DESC
            LIMIT 20
        """
    },
    "Q25: Career Trajectory Analysis": {
        "description": "Time-series analysis of player evolution",
        "sql": """
            SELECT 
                p.full_name,
                strftime('%Y-%m', m.match_date) as quarter,
                AVG(ps.runs_scored) as quarterly_avg,
                AVG(ps.strike_rate) as quarterly_sr,
                COUNT(DISTINCT m.match_id) as matches,
                CASE 
                    WHEN AVG(ps.runs_scored) > LAG(AVG(ps.runs_scored)) OVER (PARTITION BY p.player_id ORDER BY quarter) THEN 'Ascending'
                    WHEN AVG(ps.runs_scored) < LAG(AVG(ps.runs_scored)) OVER (PARTITION BY p.player_id ORDER BY quarter) THEN 'Declining'
                    ELSE 'Stable'
                END as trajectory
            FROM players p
            JOIN performance_stats ps ON p.player_id = ps.player_id
            JOIN matches m ON ps.match_id = m.match_id
            WHERE m.match_date >= DATE('now', '-2 years')
            GROUP BY p.player_id, quarter
            HAVING COUNT(DISTINCT m.match_id) >= 3
            ORDER BY p.full_name, quarter DESC
        """
    }
}


def execute_query(query: str):
    """
    Execute a SQL query and display results.
    
    Args:
        query (str): SQL query to execute.
    """
    try:
        results = db_connection.execute_query(query, fetch="all")
        
        if results:
            if isinstance(results, list) and len(results) > 0:
                # Convert results to DataFrame for better display
                if isinstance(results[0], (tuple, list)):
                    columns = [f"Col_{i}" for i in range(len(results[0]))]
                    df = pd.DataFrame(results, columns=columns)
                else:
                    df = pd.DataFrame(results)
                
                st.dataframe(df, use_container_width=True)
                st.success(f"✓ Query executed successfully ({len(results)} rows)")
            else:
                st.info("Query returned no results")
        else:
            st.info("Query executed but returned no data")
            
    except Exception as e:
        st.error(f"✗ Query execution failed: {str(e)}")
        logger.error(f"Query execution error: {str(e)}")


def execute_beginner_queries():
    """Execute and display beginner-level SQL queries (Q1-Q8)."""
    st.markdown("## Beginner Level (Q1-Q8)")
    st.markdown("*Basic SELECT, WHERE, GROUP BY, ORDER BY*")
    
    selected_query = st.selectbox(
        "Select a beginner query",
        list(BEGINNER_QUERIES.keys()),
        key="beginner_select"
    )
    
    query_info = BEGINNER_QUERIES[selected_query]
    
    st.markdown(f"**{selected_query}**: {query_info['description']}")
    st.code(query_info['sql'], language="sql")
    
    if st.button("Execute Query", key="beginner_execute"):
        execute_query(query_info['sql'])


def execute_intermediate_queries():
    """Execute and display intermediate-level SQL queries (Q9-Q16)."""
    st.markdown("## Intermediate Level (Q9-Q16)")
    st.markdown("*JOINs, subqueries, aggregate functions*")
    
    selected_query = st.selectbox(
        "Select an intermediate query",
        list(INTERMEDIATE_QUERIES.keys()),
        key="intermediate_select"
    )
    
    query_info = INTERMEDIATE_QUERIES[selected_query]
    
    st.markdown(f"**{selected_query}**: {query_info['description']}")
    st.code(query_info['sql'], language="sql")
    
    if st.button("Execute Query", key="intermediate_execute"):
        execute_query(query_info['sql'])


def execute_advanced_queries():
    """Execute and display advanced-level SQL queries (Q17-Q25)."""
    st.markdown("## Advanced Level (Q17-Q25)")
    st.markdown("*Window functions, CTEs, complex analytics*")
    
    selected_query = st.selectbox(
        "Select an advanced query",
        list(ADVANCED_QUERIES.keys()),
        key="advanced_select"
    )
    
    query_info = ADVANCED_QUERIES[selected_query]
    
    st.markdown(f"**{selected_query}**: {query_info['description']}")
    st.code(query_info['sql'], language="sql")
    
    if st.button("Execute Query", key="advanced_execute"):
        execute_query(query_info['sql'])


def custom_query_interface():
    """Provide interface for users to write and execute custom SQL queries."""
    st.markdown("## 📝 Custom Query Interface")
    
    custom_sql = st.text_area(
        "Write your own SQL query",
        height=200,
        placeholder="SELECT * FROM players LIMIT 10"
    )
    
    if st.button("Execute Custom Query", use_container_width=True):
        if custom_sql.strip():
            execute_query(custom_sql)
        else:
            st.warning("Please enter a SQL query")


if __name__ == "__main__":
    display_header()
    
    tab1, tab2, tab3, tab4 = st.tabs(["Beginner", "Intermediate", "Advanced", "Custom"])
    
    with tab1:
        execute_beginner_queries()
    
    with tab2:
        execute_intermediate_queries()
    
    with tab3:
        execute_advanced_queries()
    
    with tab4:
        custom_query_interface()
