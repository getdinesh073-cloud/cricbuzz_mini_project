# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A comprehensive cricket analytics dashboard built with Python, Streamlit, and SQL. Integrates live data from the Cricbuzz API with a SQL database to deliver real-time match updates, player statistics, and advanced analytics.

## 📋 Project Overview

**Cricbuzz LiveStats** is a full-stack web application designed for:
- **Sports Media & Broadcasting**: Real-time match updates and player analysis
- **Fantasy Cricket Platforms**: Player form analysis and performance tracking
- **Cricket Analytics Firms**: Statistical modeling and performance evaluation
- **Educational Institutions**: Learning database operations with real-world data
- **Sports Betting & Prediction**: Historical performance analysis and trend tracking

## ✨ Features

### 🏠 Home Page
- Project overview and description
- Navigation to all application modules
- Setup instructions and documentation links

### ⚡ Live Match Page
- Real-time cricket matches from Cricbuzz API
- Live scorecards with batsmen/bowler information
- Match status, venue details, and current scores
- Match history and completed matches

### 📊 Top Player Stats Page
- Top batting statistics (most runs, highest score, batting average)
- Top bowling statistics (most wickets, economy rate, bowling average)
- Filter by cricket format (Test, ODI, T20I)
- Player comparison tools

### 🔍 SQL Queries & Analytics Page
- 25+ SQL queries covering beginner to advanced levels
- Pre-built analytics queries for cricket insights
- Custom query interface for users
- Results visualization in tabular format

**Query Categories:**
- **Beginner (Q1-Q8)**: Basic SELECT, WHERE, GROUP BY, ORDER BY
- **Intermediate (Q9-Q16)**: JOINs, subqueries, aggregate functions
- **Advanced (Q17-Q25)**: Window functions, CTEs, complex analytics

### 🛠️ CRUD Operations Page
- Create new player and match records
- Read/retrieve existing records
- Update player and match information
- Delete records with form-based UI

## 🛠️ Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.x |
| **Database** | PostgreSQL / MySQL / SQLite |
| **API Integration** | Cricbuzz REST API |
| **Data Processing** | Pandas, NumPy |
| **HTTP Requests** | Requests library |

## 📦 Project Structure

```
cricbuzz_mini_project/
├── main.py                      # Entry point for Streamlit app
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── schema.sql                   # Database schema
├── .gitignore                   # Git ignore file
├── README.md                    # This file
│
├── utils/
│   ├── __init__.py              # Package initialization
│   ├── db_connection.py         # Database connection handler
│   └── api_handler.py           # Cricbuzz API integration
│
├── pages/
│   ├── 01_home.py               # Home page module
│   ├── 02_live_matches.py       # Live matches page module
│   ├── 03_player_stats.py       # Player stats page module
│   ├── 04_sql_analytics.py      # SQL analytics page module
│   └── 05_crud_operations.py    # CRUD operations page module
│
└── docs/
    ├── SETUP.md                 # Setup instructions
    ├── API_REFERENCE.md         # API integration guide
    └── SQL_QUERIES.md           # SQL queries documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Database (PostgreSQL, MySQL, or SQLite)
- Cricbuzz API Key (optional for some endpoints)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cricbuzz_mini_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   # Create database and run schema
   psql -U <user> -d <database> -f schema.sql
   ```

5. **Configure environment variables**
   ```bash
   # Create .env file
   echo "DB_HOST=localhost" > .env
   echo "DB_USER=your_user" >> .env
   echo "DB_PASSWORD=your_password" >> .env
   echo "CRICBUZZ_API_KEY=your_api_key" >> .env
   ```

6. **Run the application**
   ```bash
   streamlit run main.py
   ```

The app will open at `http://localhost:8501`

## 📊 Database Schema

The application uses the following main tables:
- **players**: Player information and metadata
- **teams**: Team details and captain information
- **venues**: Stadium and venue information
- **matches**: Match details, results, and outcomes
- **series**: Cricket series and tournament information
- **performance_stats**: Player statistics across formats
- **innings**: Batting performance details
- **bowling_performance**: Bowling statistics per match

See `schema.sql` for complete schema definition.

## 🔗 API Integration

The application integrates with the **Cricbuzz Cricket API** via REST endpoints to fetch:
- Live match data
- Player statistics
- Series information
- Match updates and scorecards

**Configuration**: Set `CRICBUZZ_API_KEY` in environment variables or `config.py`

## 💾 Database Configuration

Update `config.py` to select your database:

```python
DB_TYPE = "sqlite"      # Options: sqlite, postgresql, mysql
DB_NAME = "cricbuzz.db"
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "user"
DB_PASSWORD = "password"
```

## 📝 Coding Standards

- Follow **PEP 8** Python style guidelines
- Implement proper **exception handling** for API and database operations
- Use **secure methods** for database credentials and API keys
- Keep code **modular** with separate functions for different operations
- Add **docstrings** and comments for all functions

## 🔐 Security Considerations

- Never commit credentials to Git
- Use environment variables for sensitive data
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper error handling without exposing system details

## 📚 SQL Practice Queries

The application includes 25 SQL practice questions:

| Level | Count | Focus |
|-------|-------|-------|
| **Beginner** | 8 | Basic SELECT, filtering, sorting |
| **Intermediate** | 8 | JOINs, aggregation, subqueries |
| **Advanced** | 9 | Window functions, complex analytics |

Examples:
- Find all players from a specific country
- List top 10 run scorers across formats
- Analyze team performance (home vs away)
- Calculate player consistency metrics
- Track player form trends

See `docs/SQL_QUERIES.md` for complete query reference.

## 🎯 Key Use Cases

### For Sports Analytics Firms
- Advanced statistical modeling
- Performance trend analysis
- Data-driven player evaluation

### For Fantasy Cricket Platforms
- Real-time player form analysis
- Head-to-head statistics
- Recent performance trends

### For Educational Institutions
- Teaching SQL with real-world cricket data
- Learning API integration
- Web development with Streamlit

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Submit a Pull Request

## ⏰ Project Timeline

- **Assigned**: [Date]
- **Deadline**: 14 days from assignment
- **Submit**: Complete working dashboard with all features

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Database connection fails
- **Solution**: Verify database credentials in `.env` and `config.py`

**Issue**: API calls return errors
- **Solution**: Check API key, rate limits, and network connectivity

**Issue**: Streamlit app won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📖 Documentation

- `docs/SETUP.md`: Detailed setup instructions
- `docs/API_REFERENCE.md`: API integration guide
- `docs/SQL_QUERIES.md`: SQL queries and analytics

## 📜 License

This project is provided for educational purposes.

## 👨‍💻 Author

**Created by**: [Your Name]  
**Last Updated**: June 2026

---

**Happy Cricket Analytics! 🏏📊**

For questions or support, refer to the project documentation or contact the development team.
