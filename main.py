import customtkinter as ctk

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FinanceApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Мои финансы")
        self.window.geometry("500x400")
        
        # Заголовок
        title = ctk.CTkLabel(
            self.window, 
            text="Личные финансы", 
            font=("Arial", 28, "bold")
        )
        title.pack(pady=30)
        
        # Кнопки
        btn_frame = ctk.CTkFrame(self.window)
        btn_frame.pack(pady=20)
        
        btn_income = ctk.CTkButton(
            btn_frame, 
            text="💰 Добавить доход", 
            width=200,
            height=40
        )
        btn_income.pack(pady=10)
        
        btn_expense = ctk.CTkButton(
            btn_frame, 
            text="💸 Добавить расход", 
            width=200,
            height=40
        )
        btn_expense.pack(pady=10)
        
        btn_balance = ctk.CTkButton(
            btn_frame, 
            text="📊 Показать баланс", 
            width=200,
            height=40
        )
        btn_balance.pack(pady=10)
        
        # Метка для вывода информации
        self.info_label = ctk.CTkLabel(
            self.window, 
            text="Добро пожаловать!",
            font=("Arial", 14)
        )
        self.info_label.pack(pady=20)
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FinanceApp()
    app.run()