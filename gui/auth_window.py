import customtkinter as ctk
from services.auth_service import AuthService

class AuthWindow:
    def __init__(self, parent, db, on_login_success):
        ctk.set_appearance_mode("dark")   # 👈 гарантия тёмной темы
        self.parent = parent
        self.db = db
        self.on_login_success = on_login_success
        
        # Очищаем родительское окно
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Настройки окна
        parent.title("Финансы - Вход")
        parent.geometry("400x550")
        
        # Центральный фрейм
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(pady=30, padx=30, fill="both", expand=True)
        
        # Заголовок
        title = ctk.CTkLabel(
            self.frame, 
            text="📊 ЛИЧНЫЕ ФИНАНСЫ", 
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)
        
        # Вкладки для входа и регистрации
        self.tabview = ctk.CTkTabview(self.frame)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.login_tab = self.tabview.add("Вход")
        self.register_tab = self.tabview.add("Регистрация")
        
        # ========== ВКЛАДКА ВХОД ==========
        self.login_username = ctk.CTkEntry(
            self.login_tab, 
            placeholder_text="Имя пользователя", 
            width=250
        )
        self.login_username.pack(pady=10)
        
        self.login_password = ctk.CTkEntry(
            self.login_tab, 
            placeholder_text="Пароль", 
            show="*", 
            width=250
        )
        self.login_password.pack(pady=10)
        
        self.login_btn = ctk.CTkButton(
            self.login_tab, 
            text="Войти", 
            command=self.login, 
            width=200
        )
        self.login_btn.pack(pady=20)
        
        # ========== ВКЛАДКА РЕГИСТРАЦИЯ ==========
        self.register_username = ctk.CTkEntry(
            self.register_tab, placeholder_text="Имя пользователя", width=250
        )
        self.register_username.pack(pady=10)

        # 👇 Email теперь после логина
        self.register_email = ctk.CTkEntry(
            self.register_tab, placeholder_text="Email (обязательно)", width=250
        )
        self.register_email.pack(pady=10)

        self.register_password = ctk.CTkEntry(
            self.register_tab, placeholder_text="Пароль", show="*", width=250
        )
        self.register_password.pack(pady=10)

        self.register_confirm = ctk.CTkEntry(
            self.register_tab, placeholder_text="Повторите пароль", show="*", width=250
        )
        self.register_confirm.pack(pady=10)

        self.register_btn = ctk.CTkButton(
            self.register_tab, text="Зарегистрироваться", command=self.register, width=200
        )
        self.register_btn.pack(pady=20)
        
        # Метка для сообщений
        self.message_label = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.message_label.pack(pady=10)
    
    def show_message(self, text, color="red"):
        self.message_label.configure(text=text, text_color=color)
        self.parent.after(3000, lambda: self.message_label.configure(text=""))
    
    def login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        
        if not username or not password:
            self.show_message("Заполните все поля!")
            return
        
        user_id, username, msg = AuthService.login(self.db, username, password)
        if user_id:
            self.show_message(f"Добро пожаловать, {username}!", "green")
            self.parent.after(500, lambda: self.on_login_success(user_id, username))
        else:
            self.show_message(msg)
    
    def register(self):
        username = self.register_username.get()
        password = self.register_password.get()
        confirm = self.register_confirm.get()
        email = self.register_email.get()
        
        # Проверка заполнения полей
        if not username or not password or not email:
            self.show_message("Заполните все поля!")
            return
        
        # Проверка совпадения паролей
        if password != confirm:
            self.show_message("Пароли не совпадают!")
            return
        
        # Простая проверка корректности email
        if "@" not in email or "." not in email:
            self.show_message("Введите корректный email (пример: user@mail.ru)")
            return
        
        # Регистрация
        user_id, username, msg = AuthService.register(self.db, username, password, email)
        if user_id:
            self.show_message("Регистрация успешна! Теперь войдите.", "green")
            self.tabview.set("Вход")
            # Очищаем поля регистрации
            self.register_username.delete(0, 'end')
            self.register_password.delete(0, 'end')
            self.register_confirm.delete(0, 'end')
            self.register_email.delete(0, 'end')
        else:
            self.show_message(msg)