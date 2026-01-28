import sqlite3
import os
from datetime import datetime

class LibraryManager:
    """Gère la persistance des données dans SQLite."""
    def __init__(self, db_path="data/library.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    duration INTEGER,
                    platform TEXT,
                    local_path TEXT,
                    url TEXT,
                    added_at TIMESTAMP
                )
            """)

    def add_video(self, video_data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO videos 
                (id, title, author, duration, platform, local_path, url, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video_data['id'],
                video_data['title'],
                video_data.get('uploader', 'Inconnu'),
                video_data.get('duration', 0),
                video_data.get('extractor', 'web'),
                video_data['local_path'],
                video_data['webpage_url'],
                datetime.now().isoformat()
            ))

    def get_all_videos(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM videos ORDER BY added_at DESC")
            return [dict(row) for row in cursor.fetchall()]
