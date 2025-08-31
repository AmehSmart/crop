"""
database.py - Handles SQLite operations and data persistence for the application.
"""
import sqlite3
from typing import Any, List, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "crop_assistant.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farmland_size REAL,
                previous_crop TEXT,
                current_crop TEXT,
                soil_type TEXT,
                recommendation TEXT,
                fertilizer TEXT,
                techniques TEXT
            )
        ''')
        self.conn.commit()

    def save_user_entry(
        self,
        farmland_size: float,
        previous_crop: str,
        current_crop: str,
        soil_type: str,
        recommendation: str,
        fertilizer: str,
        techniques: str
    ):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO user_entries (
                farmland_size, previous_crop, current_crop, soil_type,
                recommendation, fertilizer, techniques
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (farmland_size, previous_crop, current_crop, soil_type, recommendation, fertilizer, techniques))
        self.conn.commit()

    def get_user_entries(self) -> List[Tuple[Any]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_entries ORDER BY id DESC')
        return cursor.fetchall()

    def close(self):
        self.conn.close()
