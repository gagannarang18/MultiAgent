from datetime import datetime
import sqlite3
from langchain.memory import ConversationBufferMemory

class SharedMemory:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self._init_db()
        self.conversation_memory = ConversationBufferMemory()
    
    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                format TEXT,
                intent TEXT,
                extracted_fields TEXT,
                timestamp DATETIME,
                conversation_id TEXT
            )
        ''')
        self.conn.commit()
    
    def log_context(self, source, format, intent, extracted_fields, conversation_id=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO context (source, format, intent, extracted_fields, timestamp, conversation_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source, format, intent, str(extracted_fields), datetime.now(), conversation_id))
        self.conn.commit()
        self.conversation_memory.save_context(
            {"input": f"New {format} processed"},
            {"output": str(extracted_fields)}
        )
    
    def get_last_context(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM context ORDER BY timestamp DESC LIMIT 1')
        return cursor.fetchone()
    
    def close(self):
        self.conn.close()