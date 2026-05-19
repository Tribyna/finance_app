import customtkinter as ctk
from services.finance_service import FinanceService
from gui.add_transaction import AddTransactionWindow
from gui.history_window import HistoryWindow

class MainWindow:
    def __init__(self, parent, db, user_id, username):
        self.parent = parent
        self.db = db
        self.user_id = user_id
        self.username = username
        
        # Очищаем родительское окно
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Настройки окна
        parent.title(f"Финансы - {username}")
        parent.geometry("900x650")
        
        # Настройка цветовой схемы (как калькулятор Windows)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Боковая панель (светло-серая)
        self.sidebar = ctk.CTkFrame(
            parent, 
            width=220, 
            corner_radius=0,
            fg_color="#f0f0f0"
        )
        self.sidebar.pack(side="left", fill="y")
        
        # Контентная область (белая)
        self.content = ctk.CTkFrame(
            parent, 
            fg_color="#ffffff"
        )
        self.content.pack(side="right", fill="both", expand=True)
        
        # Заголовок на боковой панели
        welcome = ctk.CTkLabel(
            self.sidebar, 
            text=f"👋 Здравствуйте,\n{username}!", 
            font=("Segoe UI", 16, "bold"),
            text_color="#2c3e50"
        )
        welcome.pack(pady=30)
        
        # Разделитель
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color="#d0d0d0")
        separator.pack(pady=10, padx=20, fill="x")
        
        # Кнопки меню (по центру)
        button_frame = ctk.CTkFrame(self.sidebar, fg_color="#f0f0f0")
        button_frame.pack(expand=True)
        
        self.add_income_btn = ctk.CTkButton(
            button_frame, 
            text="💰 Доход", 
            command=lambda: self.show_add_transaction("income"),
            width=180,
            height=45,
            font=("Segoe UI", 14),
            fg_color="#2ecc71",
            hover_color="#27ae60",
            corner_radius=8
        )
        self.add_income_btn.pack(pady=10)
        
        self.add_expense_btn = ctk.CTkButton(
            button_frame, 
            text="💸 Расход", 
            command=lambda: self.show_add_transaction("expense"),
            width=180,
            height=45,
            font=("Segoe UI", 14),
            fg_color="#e74c3c",
            hover_color="#c0392b",
            corner_radius=8
        )
        self.add_expense_btn.pack(pady=10)
        
        self.history_btn = ctk.CTkButton(
            button_frame, 
            text="📜 История", 
            command=self.show_history,
            width=180,
            height=45,
            font=("Segoe UI", 14),
            fg_color="#3498db",
            hover_color="#2980b9",
            corner_radius=8
        )
        self.history_btn.pack(pady=10)
        
        # Разделитель
        separator2 = ctk.CTkFrame(self.sidebar, height=2, fg_color="#d0d0d0")
        separator2.pack(pady=10, padx=20, fill="x")
        
        self.logout_btn = ctk.CTkButton(
            self.sidebar, 
            text="🚪 Выход", 
            command=self.logout,
            width=180,
            height=40,
            font=("Segoe UI", 13),
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            corner_radius=8
        )
        self.logout_btn.pack(pady=10)
        
        # Показываем дашборд
        self.show_dashboard()
    
    def show_dashboard(self):
        # Очищаем контент
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Получаем данные
        balance = FinanceService.get_balance(self.db, self.user_id)
        income_total = FinanceService.get_income_total(self.db, self.user_id)
        expense_total = FinanceService.get_expense_total(self.db, self.user_id)
        
        # Главный фрейм для центрирования
        main_frame = ctk.CTkFrame(self.content, fg_color="#ffffff")
        main_frame.pack(expand=True)
        
        # Заголовок
        title = ctk.CTkLabel(
            main_frame, 
            text="Финансовый дашборд", 
            font=("Segoe UI", 24, "bold"),
            text_color="#2c3e50"
        )
        title.pack(pady=(0, 30))
        
        # Карточка баланса (центрированная)
        balance_frame = ctk.CTkFrame(
            main_frame, 
            fg_color="#f8f9fa",
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0"
        )
        balance_frame.pack(pady=10, padx=30)
        
        balance_label = ctk.CTkLabel(
            balance_frame, 
            text="ТЕКУЩИЙ БАЛАНС", 
            font=("Segoe UI", 14),
            text_color="#7f8c8d"
        )
        balance_label.pack(pady=(15, 5))
        
        balance_amount = ctk.CTkLabel(
            balance_frame, 
            text=f"{balance:,.2f} ₽", 
            font=("Segoe UI", 32, "bold")
        )
        balance_amount.pack(pady=(0, 15))
        
        # Цвет баланса
        if balance >= 0:
            balance_amount.configure(text_color="#2ecc71")
        else:
            balance_amount.configure(text_color="#e74c3c")
        
        # Статистика (доходы и расходы в ряд)
        stats_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        stats_frame.pack(pady=20)
        
        # Доходы (слева)
        income_frame = ctk.CTkFrame(
            stats_frame, 
            fg_color="#f8f9fa",
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0",
            width=250,
            height=120
        )
        income_frame.pack(side="left", padx=15)
        income_frame.pack_propagate(False)
        
        income_emoji = ctk.CTkLabel(
            income_frame, 
            text="📈", 
            font=("Segoe UI", 28),
            text_color="#2ecc71"
        )
        income_emoji.pack(pady=(15, 0))
        
        income_label = ctk.CTkLabel(
            income_frame, 
            text="ДОХОДЫ", 
            font=("Segoe UI", 12),
            text_color="#7f8c8d"
        )
        income_label.pack()
        
        income_amount = ctk.CTkLabel(
            income_frame, 
            text=f"{income_total:,.2f} ₽", 
            font=("Segoe UI", 20, "bold"),
            text_color="#2ecc71"
        )
        income_amount.pack(pady=(0, 15))
        
        # Расходы (справа)
        expense_frame = ctk.CTkFrame(
            stats_frame, 
            fg_color="#f8f9fa",
            corner_radius=15,
            border_width=1,
            border_color="#e0e0e0",
            width=250,
            height=120
        )
        expense_frame.pack(side="right", padx=15)
        expense_frame.pack_propagate(False)
        
        expense_emoji = ctk.CTkLabel(
            expense_frame, 
            text="📉", 
            font=("Segoe UI", 28),
            text_color="#e74c3c"
        )
        expense_emoji.pack(pady=(15, 0))
        
        expense_label = ctk.CTkLabel(
            expense_frame, 
            text="РАСХОДЫ", 
            font=("Segoe UI", 12),
            text_color="#7f8c8d"
        )
        expense_label.pack()
        
        expense_amount = ctk.CTkLabel(
            expense_frame, 
            text=f"{expense_total:,.2f} ₽", 
            font=("Segoe UI", 20, "bold"),
            text_color="#e74c3c"
        )
        expense_amount.pack(pady=(0, 15))
    
    def show_add_transaction(self, trans_type):
        AddTransactionWindow(
            self.parent, 
            self.db, 
            self.user_id, 
            trans_type, 
            self.show_dashboard
        )
    
    def show_history(self):
        HistoryWindow(self.parent, self.db, self.user_id)
    
    def logout(self):
        from gui.auth_window import AuthWindow
        AuthWindow(self.parent, self.db, self.on_login_success)
    
    def on_login_success(self, user_id, username):
        MainWindow(self.parent, self.db, user_id, username)