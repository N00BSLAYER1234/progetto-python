"""
Database module for handling user authentication and high scores
"""
import sqlite3
import hashlib
from typing import Optional, List, Tuple


class Database:
    def __init__(self, db_name: str = "game_data.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_name = db_name
        self.create_tables()
    
    def get_connection(self):
        """Get a database connection"""
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        """Create necessary tables for users and scores"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level INTEGER NOT NULL,
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        if not username or not password:
            return False, "Username and password cannot be empty"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            return True, "Registration successful!"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        finally:
            conn.close()
    
    def login_user(self, username: str, password: str) -> Optional[int]:
        """
        Verify user credentials and return user ID if successful
        Returns: user_id if successful, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def save_score(self, user_id: int, score: int, level: int):
        """Save a user's score for a specific level"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO scores (user_id, score, level) VALUES (?, ?, ?)",
            (user_id, score, level)
        )
        
        conn.commit()
        conn.close()
    
    def get_user_high_score(self, user_id: int) -> int:
        """Get the highest score for a specific user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT MAX(score) FROM scores WHERE user_id = ?",
            (user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0
    
    def get_global_high_score(self) -> Tuple[int, str]:
        """
        Get the global high score and username
        Returns: (score, username)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT MAX(s.score), u.username
            FROM scores s
            JOIN users u ON s.user_id = u.id
            GROUP BY s.user_id
            ORDER BY MAX(s.score) DESC
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return result[0], result[1]
        return 0, "None"
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int]]:
        """
        Get top scores across all users
        Returns: List of (username, score) tuples
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.username, MAX(s.score) as high_score
            FROM scores s
            JOIN users u ON s.user_id = u.id
            GROUP BY s.user_id
            ORDER BY high_score DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return results