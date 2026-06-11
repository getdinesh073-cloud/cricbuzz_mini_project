"""
Database Connection Module

Centralized database connection handling for Cricbuzz LiveStats.
Supports PostgreSQL, MySQL, and SQLite (database-agnostic design).
Provides connection pooling and safe query execution.
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Any, List, Tuple, Optional

import config

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(config.LOG_LEVEL)

# Connection pools (simple singleton pattern)
_db_connection = None


def get_db_connection():
    """
    Establish and return a database connection.
    Uses singleton pattern to reuse connections.
    
    Returns:
        Connection object for the configured database.
        
    Raises:
        ConnectionError: If connection cannot be established.
    """
    global _db_connection
    
    try:
        if config.DB_TYPE == "sqlite":
            _db_connection = sqlite3.connect(config.DB_NAME, timeout=config.DB_TIMEOUT)
            _db_connection.row_factory = sqlite3.Row  # Return rows as dictionaries
            logger.info(f"✓ Connected to SQLite database: {config.DB_NAME}")
            
        elif config.DB_TYPE == "postgresql":
            try:
                import psycopg2
            except ImportError:
                raise ImportError("psycopg2 not installed. Run: pip install psycopg2-binary")
            
            _db_connection = psycopg2.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                connect_timeout=config.DB_TIMEOUT,
            )
            logger.info(f"✓ Connected to PostgreSQL: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
            
        elif config.DB_TYPE == "mysql":
            try:
                import mysql.connector
            except ImportError:
                raise ImportError("mysql-connector-python not installed. Run: pip install mysql-connector-python")
            
            _db_connection = mysql.connector.connect(
                host=config.DB_HOST,
                port=config.DB_PORT,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                database=config.DB_NAME,
                connection_timeout=config.DB_TIMEOUT,
            )
            logger.info(f"✓ Connected to MySQL: {config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}")
        
        return _db_connection
        
    except Exception as e:
        logger.error(f"✗ Database connection failed: {str(e)}")
        raise ConnectionError(f"Failed to connect to {config.DB_TYPE} database: {str(e)}")


@contextmanager
def get_db_cursor():
    """
    Context manager for database cursor operations.
    Automatically commits on success, rolls back on error.
    
    Yields:
        Cursor object for executing queries.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        yield cursor
        conn.commit()
        logger.debug("✓ Transaction committed")
    except Exception as e:
        conn.rollback()
        logger.error(f"✗ Transaction rolled back: {str(e)}")
        raise
    finally:
        cursor.close()


def execute_query(query: str, params: Tuple = None, fetch: str = "all") -> Any:
    """
    Execute a SQL query and return results.
    
    Args:
        query (str): SQL query string.
        params (tuple): Query parameters for parameterized queries.
        fetch (str): 'all' for all rows, 'one' for first row, 'none' for insert/update/delete.
        
    Returns:
        Query results (list of rows, single row, or affected rows count).
        
    Raises:
        Exception: If query execution fails.
    """
    try:
        with get_db_cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch == "all":
                results = cursor.fetchall()
                logger.debug(f"✓ Query returned {len(results)} rows")
                return results
            elif fetch == "one":
                result = cursor.fetchone()
                logger.debug("✓ Query returned 1 row")
                return result
            else:  # 'none' for INSERT/UPDATE/DELETE
                affected = cursor.rowcount
                logger.debug(f"✓ Query affected {affected} rows")
                return affected
                
    except Exception as e:
        logger.error(f"✗ Query execution failed: {str(e)}\nQuery: {query}")
        raise


def execute_many(query: str, data: List[Tuple]) -> int:
    """
    Execute multiple queries with different parameters (batch insert/update).
    
    Args:
        query (str): SQL query template.
        data (list): List of parameter tuples.
        
    Returns:
        int: Number of affected rows.
    """
    try:
        with get_db_cursor() as cursor:
            cursor.executemany(query, data)
            affected = cursor.rowcount
            logger.info(f"✓ Batch executed: {affected} rows affected")
            return affected
            
    except Exception as e:
        logger.error(f"✗ Batch execution failed: {str(e)}")
        raise


def create_table_if_not_exists(table_name: str, schema: str) -> bool:
    """
    Create a table if it doesn't already exist.
    
    Args:
        table_name (str): Table name.
        schema (str): CREATE TABLE SQL statement.
        
    Returns:
        bool: True if table created, False if already exists.
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(schema)
            logger.info(f"✓ Table '{table_name}' created or already exists")
            return True
    except Exception as e:
        logger.warning(f"⚠ Table creation: {str(e)}")
        return False


def drop_table(table_name: str) -> bool:
    """
    Drop a table (CAUTION: Data loss operation).
    
    Args:
        table_name (str): Table name to drop.
        
    Returns:
        bool: True if successful.
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            logger.warning(f"⚠ Table '{table_name}' dropped")
            return True
    except Exception as e:
        logger.error(f"✗ Drop table failed: {str(e)}")
        raise


def close_connection() -> None:
    """
    Close database connection safely.
    """
    global _db_connection
    
    try:
        if _db_connection:
            _db_connection.close()
            _db_connection = None
            logger.info("✓ Database connection closed")
    except Exception as e:
        logger.error(f"✗ Error closing connection: {str(e)}")


def get_row_count(table_name: str) -> int:
    """
    Get the number of rows in a table.
    
    Args:
        table_name (str): Table name.
        
    Returns:
        int: Row count.
    """
    try:
        result = execute_query(f"SELECT COUNT(*) FROM {table_name}")
        if config.DB_TYPE == "sqlite":
            return result[0][0]
        else:
            return result[0][0]
    except Exception as e:
        logger.error(f"✗ Failed to get row count: {str(e)}")
        return 0


def table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database.
    
    Args:
        table_name (str): Table name.
        
    Returns:
        bool: True if table exists, False otherwise.
    """
    try:
        if config.DB_TYPE == "sqlite":
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            result = execute_query(query, (table_name,))
            return len(result) > 0
        elif config.DB_TYPE == "postgresql":
            query = "SELECT to_regclass(%s)"
            result = execute_query(query, (table_name,))
            return result[0][0] is not None
        elif config.DB_TYPE == "mysql":
            query = "SELECT 1 FROM information_schema.tables WHERE table_name=%s"
            result = execute_query(query, (table_name,))
            return len(result) > 0
    except Exception as e:
        logger.error(f"✗ Table exists check failed: {str(e)}")
        return False


# Initialization on module import
if __name__ != "__main__":
    try:
        get_db_connection()
    except Exception as e:
        logger.warning(f"⚠ Database connection not established at module load: {str(e)}")
