import sqlite3
import bcrypt
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="finance.db"):
        """Подключается к БД и создаёт таблицы при первом запуске"""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Создаёт таблицы users и transactions, если их нет"""
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица транзакций
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.connection.commit()
    
    def create_user(self, username, password):
        """Создаёт нового пользователя. Возвращает True/False"""
        # Хешируем пароль
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_user(self, username):
        """Возвращает (id, username, password_hash) или None"""
        self.cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        )
        return self.cursor.fetchone()
    
    def add_transaction(self, user_id, amount, category, date, description=""):
        """Добавляет транзакцию"""
        self.cursor.execute('''
            INSERT INTO transactions (user_id, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, amount, category, date, description))
        self.connection.commit()
    
    def get_transactions(self, user_id):
        """Возвращает все транзакции пользователя"""
        self.cursor.execute(
            "SELECT id, user_id, amount, category, date, description FROM transactions WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )
        return self.cursor.fetchall()
    
    def get_balance(self, user_id):
        """Возвращает баланс пользователя"""
        self.cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE user_id = ?",
            (user_id,)
        )
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0
    
    def close(self):
        """Закрывает соединение с БД"""
        self.connection.close()