from datetime import datetime

class FinanceService:
    @staticmethod
    def add_income(db, user_id, amount, category, date=None, description=""):
        """
        Добавляет доход.
        amount - положительное число
        """
        if amount <= 0:
            return False, "Сумма должна быть положительной"
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        db.add_transaction(user_id, amount, category, date, description)
        return True, "Доход добавлен"
    
    @staticmethod
    def add_expense(db, user_id, amount, category, date=None, description=""):
        """
        Добавляет расход.
        amount - положительное число (внутри превратится в отрицательное)
        """
        if amount <= 0:
            return False, "Сумма должна быть положительной"
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Расход сохраняем как отрицательное число
        db.add_transaction(user_id, -amount, category, date, description)
        return True, "Расход добавлен"
    
    @staticmethod
    def get_balance(db, user_id):
        """Возвращает текущий баланс"""
        return db.get_balance(user_id)
    
    @staticmethod
    def get_transactions(db, user_id):
        """Возвращает все транзакции пользователя"""
        return db.get_transactions(user_id)
    
    @staticmethod
    def get_income_total(db, user_id):
        """Возвращает сумму всех доходов"""
        transactions = db.get_transactions(user_id)
        total = sum(t[2] for t in transactions if t[2] > 0)
        return total
    
    @staticmethod
    def get_expense_total(db, user_id):
        """Возвращает сумму всех расходов (положительное число)"""
        transactions = db.get_transactions(user_id)
        total = sum(-t[2] for t in transactions if t[2] < 0)
        return total