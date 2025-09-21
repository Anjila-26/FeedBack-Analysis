import sqlite3
import json
from pathlib import Path
from typing import List, Optional
from models.feedback import Feedback
from contextlib import contextmanager

DATABASE_PATH = "feedback.db"

def init_database():
    """Initialize the database with required tables."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
                comment TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                category TEXT DEFAULT 'general'
            )
        """)
        conn.commit()

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def insert_feedback(feedback: Feedback) -> int:
    """Insert feedback into database and return the ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (user_id, rating, comment, timestamp, category)
            VALUES (?, ?, ?, ?, ?)
        """, (
            feedback.user_id,
            feedback.rating,
            feedback.comment,
            feedback.timestamp,
            feedback.category
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_feedback() -> List[Feedback]:
    """Retrieve all feedback from database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, rating, comment, timestamp, category
            FROM feedback
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()

        return [
            Feedback(
                user_id=row[0],
                rating=row[1],
                comment=row[2],
                timestamp=row[3],
                category=row[4]
            )
            for row in rows
        ]

def get_feedback_by_id(feedback_id: int) -> Optional[Feedback]:
    """Get specific feedback by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, rating, comment, timestamp, category
            FROM feedback
            WHERE id = ?
        """, (feedback_id,))
        row = cursor.fetchone()

        if row:
            return Feedback(
                user_id=row[0],
                rating=row[1],
                comment=row[2],
                timestamp=row[3],
                category=row[4]
            )
        return None

def get_feedback_count() -> int:
    """Get total count of feedback entries."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feedback")
        return cursor.fetchone()[0]

def get_feedback_statistics():
    """Get basic statistics from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Average rating
        cursor.execute("SELECT AVG(rating) FROM feedback")
        avg_rating = cursor.fetchone()[0] or 0

        # Category breakdown
        cursor.execute("SELECT category, COUNT(*) FROM feedback GROUP BY category")
        category_counts = dict(cursor.fetchall())

        # Total count
        total_count = get_feedback_count()

        return {
            "total_feedback": total_count,
            "average_rating": round(avg_rating, 2),
            "category_breakdown": category_counts
        }