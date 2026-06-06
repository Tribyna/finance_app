import customtkinter as ctk
from services.finance_service import FinanceService

class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, parent, db, user_id):
        super().__init__(parent)
        self.db = db
        self.user_id = user_id
        
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        
        self.title("История операций")
        self.geometry("850x500")
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.configure(fg_color="#ffffff")
        
        headers_frame = ctk.CTkFrame(self, fg_color="#f0f0f0", corner_radius=10)
        headers_frame.pack(pady=10, padx=10, fill="x")
        
        headers = ["Дата", "Тип", "Сумма", "Категория", "Описание"]
        widths = [100, 80, 120, 150, 250]
        
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                headers_frame, 
                text=header, 
                font=("Segoe UI", 14, "bold"),
                text_color="#2c3e50",
                width=width
            )
            label.grid(row=0, column=i, padx=5, pady=8)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="#ffffff",
            border_width=0
        )
        self.scrollable_frame.pack(pady=5, padx=10, fill="both", expand=True)
        
        self.load_transactions()
    
    def load_transactions(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        transactions = FinanceService.get_transactions(self.db, self.user_id)
        
        if not transactions:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame, 
                text="📭 Нет операций",
                font=("Segoe UI", 16),
                text_color="#7f8c8d"
            )
            empty_label.pack(pady=50)
            return
        
        for i, t in enumerate(transactions):
            _, _, amount, category, date, desc, created_at = t
            
            type_str = "Доход" if amount > 0 else "Расход"
            amount_str = f"{amount:,.2f} ₽"
            amount_color = "#2ecc71" if amount > 0 else "#e74c3c"
            type_color = "#2ecc71" if amount > 0 else "#e74c3c"
            
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            
            row_frame = ctk.CTkFrame(self.scrollable_frame, fg_color=bg_color, corner_radius=5)
            row_frame.pack(fill="x", pady=2)
            
            date_label = ctk.CTkLabel(
                row_frame, 
                text=date, 
                width=100,
                font=("Segoe UI", 13),
                text_color="#2c3e50"
            )
            date_label.pack(side="left", padx=5, pady=8)
            
            type_label = ctk.CTkLabel(
                row_frame, 
                text=type_str, 
                width=80,
                font=("Segoe UI", 13, "bold"),
                text_color=type_color
            )
            type_label.pack(side="left", padx=5, pady=8)
            
            amount_label = ctk.CTkLabel(
                row_frame, 
                text=amount_str, 
                width=120,
                font=("Segoe UI", 13, "bold"),
                text_color=amount_color
            )
            amount_label.pack(side="left", padx=5, pady=8)
            
            category_label = ctk.CTkLabel(
                row_frame, 
                text=category, 
                width=150,
                font=("Segoe UI", 13),
                text_color="#2c3e50"
            )
            category_label.pack(side="left", padx=5, pady=8)
            
            desc_text = desc if desc else "—"
            desc_color = "#7f8c8d" if not desc else "#2c3e50"
            desc_label = ctk.CTkLabel(
                row_frame, 
                text=desc_text, 
                width=250,
                font=("Segoe UI", 13),
                text_color=desc_color,
                anchor="w"
            )
            desc_label.pack(side="left", padx=5, pady=8)