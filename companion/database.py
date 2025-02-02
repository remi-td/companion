# database.py

import sqlite3
import threading

class Database:
    _instance_lock = threading.Lock()

    def __new__(cls, db_path='data/chat_history.db'):
        print('*****START DATABASE****')
        if not hasattr(cls, '_instance'):
            with cls._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance.conn = sqlite3.connect(db_path, check_same_thread=False)
                    cls._instance.create_tables()
        return cls._instance

    def __init__(self):
        # If the database already exists, do a bit of cleanup on start..
        self._instance.delete_empty_chats()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id INTEGER,
                role TEXT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(thread_id) REFERENCES chat_threads(id)
            )
        ''')
        self.conn.commit()

    def create_thread(self, title):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO chat_threads (title) VALUES (?)', (title,))
        self.conn.commit()
        return cursor.lastrowid

    def get_threads(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, title FROM chat_threads ORDER BY created_at DESC')
        return cursor.fetchall()

    def save_message(self, thread_id, role, content):
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)',
            (thread_id, role, content)
        )
        self.conn.commit()

    def get_messages(self, thread_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT role, content FROM messages WHERE thread_id = ? ORDER BY timestamp',
            (thread_id,)
        )
        return cursor.fetchall()
    
    def get_thread_title(self, thread_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT title FROM chat_threads WHERE id = ?', (thread_id,))
        result = cursor.fetchone()
        return result[0] if result else 'New Chat'    
    
    def update_thread_title(self, thread_id, new_title):
        """
        Update the title of a chat thread.

        Args:
            thread_id (int): The ID of the chat thread.
            new_title (str): The new title for the chat thread.
        """
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE chat_threads SET title = ? WHERE id = ?',
            (new_title, thread_id)
        )
        self.conn.commit()    

    def delete_empty_chats(self):
        """
        Delete chat threads that have no associated messages.
        """
        print('CALLED CLEANUP PROC')
        cursor = self.conn.cursor()
        # Find thread IDs with no messages
        cursor.execute('''
            SELECT id FROM chat_threads
            WHERE id NOT IN (SELECT DISTINCT thread_id FROM messages)
        ''')
        empty_threads = cursor.fetchall()
        if empty_threads:
            print('DELETE THREADS:')
            print(empty_threads)
            empty_thread_ids = [thread_id[0] for thread_id in empty_threads]
            # Delete empty chat threads
            cursor.executemany(
                'DELETE FROM chat_threads WHERE id = ?',
                [(thread_id,) for thread_id in empty_thread_ids]
            )
            self.conn.commit()        