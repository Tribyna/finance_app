import customtkinter as ctk
from database.db_manager import DatabaseManager
from gui.auth_window import AuthWindow

# Настройка темы CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FinanceApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Личные финансы")
        self.root.geometry("800x600")
        
        # Подключаемся к БД
        self.db = DatabaseManager("finance.db")
        
        # Показываем окно авторизации
        self.auth_window = AuthWindow(self.root, self.db, self.on_login_success)
    
    def on_login_success(self, user_id, username):
        from gui.main_window import MainWindow
        self.main_window = MainWindow(self.root, self.db, user_id, username)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FinanceApp()
    app.run()