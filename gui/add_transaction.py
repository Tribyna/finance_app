import customtkinter as ctk
from datetime import datetime
from services.finance_service import FinanceService

class AddTransactionWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, user_id, trans_type, refresh_callback):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        self.trans_type = trans_type
        self.refresh_callback = refresh_callback
        
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        
        title = "Добавить доход" if trans_type == "income" else "Добавить расход"
        self.title(title)
        self.geometry("400x500")
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        income_categories = ["Зарплата", "Фриланс", "Подарок", "Возврат долга", "Другое"]
        expense_categories = ["Еда", "Транспорт", "Жильё", "Развлечения", "Здоровье", "Другое"]
        
        self.categories = income_categories if trans_type == "income" else expense_categories
        
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Сумма", width=250)
        self.amount_entry.pack(pady=10)
        
        self.category_combo = ctk.CTkComboBox(self, values=self.categories, width=250)
        self.category_combo.pack(pady=10)
        self.category_combo.set("Выберите категорию")
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_entry = ctk.CTkEntry(self, placeholder_text=f"Дата (YYYY-MM-DD) | {today}", width=250)
        self.date_entry.pack(pady=10)
        
        self.desc_entry = ctk.CTkEntry(self, placeholder_text="Описание (необязательно)", width=250)
        self.desc_entry.pack(pady=10)
        
        btn_text = "➕ Добавить доход" if trans_type == "income" else "➖ Добавить расход"
        btn_color = "green" if trans_type == "income" else "orange"
        
        self.save_btn = ctk.CTkButton(
            self, 
            text=btn_text, 
            command=self.save_transaction, 
            fg_color=btn_color,
            width=200
        )
        self.save_btn.pack(pady=20)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)
    
    def save_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            
            category = self.category_combo.get()
            if category == "Выберите категорию":
                raise ValueError("Выберите категорию")
            
            date = self.date_entry.get()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            description = self.desc_entry.get()
            
            if self.trans_type == "income":
                success, msg = FinanceService.add_income(
                    self.db, self.user_id, amount, category, date, description
                )
            else:
                success, msg = FinanceService.add_expense(
                    self.db, self.user_id, amount, category, date, description
                )
            
            if success:
                self.refresh_callback()
                self.destroy()
            else:
                self.error_label.configure(text=msg)
                
        except ValueError as e:
            self.error_label.configure(text=str(e))