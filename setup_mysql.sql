-- Cricbuzz LiveStats Database Setup for MySQL (XAMPP)
-- Run this script in MySQL Workbench or phpMyAdmin to create the database and tables

-- Create Database
CREATE DATABASE IF NOT EXISTS cricbuzz_db;
USE cricbuzz_db;

-- Drop existing tables if they exist (for fresh setup)
DROP TABLE IF EXISTS bowling_performance;
DROP TABLE IF EXISTS innings;
DROP TABLE IF EXISTS performance_stats;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS series;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS teams;
DROP TABLE IF EXISTS players;

-- Players Table
CREATE TABLE players (
    player_id INT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    playing_role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_country (country),
    INDEX idx_role (playing_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Teams Table
CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100),
    captain_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (captain_id) REFERENCES players(player_id) ON DELETE SET NULL,
    INDEX idx_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Venues Table
CREATE TABLE venues (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_country (country)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Matches Table
CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    description VARCHAR(500),
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    venue_id INT,
    match_date DATE,
    match_type VARCHAR(50),
    winning_team_id INT,
    victory_margin INT,
    victory_type VARCHAR(20),
    toss_winner_id INT,
    toss_decision VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team1_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (team2_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE SET NULL,
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id) ON DELETE SET NULL,
    INDEX idx_match_date (match_date),
    INDEX idx_match_type (match_type),
    INDEX idx_team1 (team1_id),
    INDEX idx_team2 (team2_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Series Table
CREATE TABLE series (
    series_id INT PRIMARY KEY,
    series_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE,
    host_country VARCHAR(100),
    series_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_start_date (start_date),
    INDEX idx_series_type (series_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance Stats Table
CREATE TABLE performance_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    match_id INT,
    format VARCHAR(20),
    matches_played INT DEFAULT 0,
    runs_scored INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    average DECIMAL(10, 2),
    strike_rate DECIMAL(10, 2),
    economy_rate DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE SET NULL,
    INDEX idx_player (player_id),
    INDEX idx_format (format),
    INDEX idx_match (match_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Innings Table
CREATE TABLE innings (
    inning_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    team_id INT NOT NULL,
    batting_order INT,
    runs_scored INT DEFAULT 0,
    wickets_lost INT DEFAULT 0,
    overs_played DECIMAL(5, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,
    INDEX idx_match (match_id),
    INDEX idx_team (team_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Bowling Performance Table
CREATE TABLE bowling_performance (
    bowling_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    overs_bowled DECIMAL(5, 1),
    runs_conceded INT DEFAULT 0,
    wickets INT DEFAULT 0,
    economy_rate DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    INDEX idx_match (match_id),
    INDEX idx_player (player_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample Data Insertion
INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style, date_of_birth) VALUES
(1, 'Virat Kohli', 'India', 'Batsman', 'Right-handed', NULL, '1988-11-05'),
(2, 'Jasprit Bumrah', 'India', 'Bowler', NULL, 'Right-arm Fast', '1993-12-06'),
(3, 'Steve Smith', 'Australia', 'Batsman', 'Right-handed', NULL, '1989-06-17'),
(4, 'Pat Cummins', 'Australia', 'Bowler', NULL, 'Right-arm Fast', '1993-01-08'),
(5, 'Kane Williamson', 'New Zealand', 'Batsman', 'Right-handed', NULL, '1990-08-08'),
(6, 'Trent Boult', 'New Zealand', 'Bowler', NULL, 'Left-arm Fast', '1989-07-22');

INSERT INTO teams (team_id, team_name, country, captain_id) VALUES
(1, 'India', 'India', 1),
(2, 'Australia', 'Australia', 3),
(3, 'New Zealand', 'New Zealand', 5);

INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1, 'Eden Gardens', 'Kolkata', 'India', 66000),
(2, 'MCG', 'Melbourne', 'Australia', 100024),
(3, 'Basin Reserve', 'Wellington', 'New Zealand', 7500);

INSERT INTO series (series_id, series_name, start_date, end_date, host_country, series_type) VALUES
(1, 'India vs Australia 2024', '2024-01-15', '2024-02-15', 'India', 'Test'),
(2, 'New Zealand Tour 2024', '2024-03-01', '2024-03-31', 'New Zealand', 'ODI');

-- Display confirmation
SELECT '✓ Database setup complete!' as status;
SELECT COUNT(*) as players_count FROM players;
SELECT COUNT(*) as teams_count FROM teams;
SELECT COUNT(*) as venues_count FROM venues;
