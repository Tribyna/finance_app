import sqlite3
import bcrypt
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="finance.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()
    
    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                is_blocked INTEGER DEFAULT 0,
                unblock_token TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
       
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                attempt_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.connection.commit()
    
    def create_user(self, username, password, email):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, username):
        self.cursor.execute(
            "SELECT id, username, password_hash, email, is_blocked FROM users WHERE username = ?",
            (username,)
        )
        return self.cursor.fetchone()
    
    def add_transaction(self, user_id, amount, category, date, description=""):
        from datetime import datetime
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('''
            INSERT INTO transactions (user_id, amount, category, date, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, amount, category, date, description, created_at))
        self.connection.commit()
    
    def get_transactions(self, user_id):
        self.cursor.execute(
            "SELECT id, user_id, amount, category, date, description, created_at FROM transactions WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def get_balance(self, user_id):
        self.cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0
    
    def close(self):
        self.connection.close()
    
    def get_user_by_email(self, email):
        self.cursor.execute("SELECT id, username FROM users WHERE email = ?", (email,))
        return self.cursor.fetchone()

    def get_failed_attempts_count(self, user_id):
        self.cursor.execute('''
            SELECT COUNT(*) FROM login_attempts 
            WHERE user_id = ? AND attempt_time > datetime('now', '-5 minutes')
        ''', (user_id,))
        return self.cursor.fetchone()[0]

    def add_failed_attempt(self, user_id):
        self.cursor.execute(
            "INSERT INTO login_attempts (user_id, attempt_time) VALUES (?, datetime('now'))",
            (user_id,)
        )
        self.connection.commit()

    def clear_failed_attempts(self, user_id):
        self.cursor.execute("DELETE FROM login_attempts WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def block_user(self, user_id):
        self.cursor.execute(
            "UPDATE users SET is_blocked = 1 WHERE id = ?",
            (user_id,)
        )
        self.connection.commit()

    def is_user_blocked(self, user_id):
        self.cursor.execute(
            "SELECT is_blocked FROM users WHERE id = ? AND is_blocked = 1",
            (user_id,)
        )
        return self.cursor.fetchone() is not None

    def save_unblock_token(self, user_id, token):
        self.cursor.execute(
            "UPDATE users SET unblock_token = ? WHERE id = ?",
            (token, user_id)
        )
        self.connection.commit()

    def unblock_user_by_token(self, token):
        self.cursor.execute(
            "UPDATE users SET is_blocked = 0, unblock_token = NULL WHERE unblock_token = ?",
            (token,)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0