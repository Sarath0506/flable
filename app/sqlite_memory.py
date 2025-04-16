import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_name='research_history.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.init_database()

    def init_database(self):
        """Initialize database connection and create table if it doesn't exist"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                response TEXT NOT NULL,
                sources TEXT,  -- Store sources as JSON
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_research(self, question, response):
        """Save new research entry to database"""
        self.cursor.execute('''
            INSERT INTO research_history (question, response)
            VALUES (?, ?)
        ''', (question, response))
        self.conn.commit()

    def view_history(self):
        """Retrieve all research history"""
        self.cursor.execute('SELECT * FROM research_history')
        return self.cursor.fetchall()


    def delete_entry(self, entry_id):
        """Delete a specific research entry"""
        try:
            self.cursor.execute('DELETE FROM research_history WHERE id = ?', (entry_id,))
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False

    def close_connection(self):
        """Close database connection"""
        if self.conn:
            self.conn.close() 