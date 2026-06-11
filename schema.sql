-- Cricbuzz LiveStats Database Schema
-- Supports PostgreSQL, MySQL, SQLite
-- Create tables for cricket analytics platform

-- Players Table
CREATE TABLE players (
    player_id INT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    playing_role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    date_of_birth DATE
);

-- Teams Table
CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    captain_id INT FOREIGN KEY REFERENCES players(player_id)
);

-- Venues Table
CREATE TABLE venues (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

-- Matches Table
CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    description VARCHAR(500),
    team1_id INT FOREIGN KEY REFERENCES teams(team_id),
    team2_id INT FOREIGN KEY REFERENCES teams(team_id),
    venue_id INT FOREIGN KEY REFERENCES venues(venue_id),
    match_date DATE,
    match_type VARCHAR(50),
    winning_team_id INT FOREIGN KEY REFERENCES teams(team_id),
    victory_margin INT,
    victory_type VARCHAR(20),
    toss_winner_id INT FOREIGN KEY REFERENCES teams(team_id),
    toss_decision VARCHAR(50)
);

-- Series Table
CREATE TABLE series (
    series_id INT PRIMARY KEY,
    series_name VARCHAR(255) NOT NULL,
    host_country VARCHAR(100),
    match_type VARCHAR(50),
    start_date DATE,
    end_date DATE,
    total_matches INT
);

-- Performance Stats Table
CREATE TABLE performance_stats (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT FOREIGN KEY REFERENCES players(player_id),
    match_id INT FOREIGN KEY REFERENCES matches(match_id),
    format VARCHAR(20),
    runs_scored INT,
    batting_average DECIMAL(10, 2),
    strike_rate DECIMAL(10, 2),
    wickets_taken INT,
    bowling_average DECIMAL(10, 2),
    economy_rate DECIMAL(10, 2),
    catches INT,
    stumpings INT,
    run_outs INT
);

-- Innings Table
CREATE TABLE innings (
    innings_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT FOREIGN KEY REFERENCES matches(match_id),
    batting_team_id INT FOREIGN KEY REFERENCES teams(team_id),
    batting_order INT,
    player_id INT FOREIGN KEY REFERENCES players(player_id),
    runs INT,
    balls_faced INT,
    batting_position INT
);

-- Bowling Performance Table
CREATE TABLE bowling_performance (
    bowling_id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT FOREIGN KEY REFERENCES matches(match_id),
    bowler_id INT FOREIGN KEY REFERENCES players(player_id),
    overs_bowled DECIMAL(5, 1),
    runs_conceded INT,
    wickets INT,
    economy_rate DECIMAL(10, 2)
);

-- Create indexes for performance optimization
CREATE INDEX idx_player_country ON players(country);
CREATE INDEX idx_team_country ON teams(country);
CREATE INDEX idx_match_date ON matches(match_date);
CREATE INDEX idx_match_venue ON matches(venue_id);
CREATE INDEX idx_performance_player ON performance_stats(player_id);
CREATE INDEX idx_performance_match ON performance_stats(match_id);
