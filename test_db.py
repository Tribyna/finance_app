from database.db_manager import DatabaseManager

db = DatabaseManager("finance.db")

# Создаём пользователя
print("Создаём пользователя 'alice':")
if db.create_user("alice", "pass123"):
    print("✅ Успешно")
else:
    print("❌ Ошибка")

# Проверяем вход
user = db.get_user("alice")
if user:
    print(f"✅ Пользователь найден: id={user[0]}, username={user[1]}")

# Добавляем транзакции
db.add_transaction(user[0], 5000, "Зарплата", "2025-05-14", "Аванс")
db.add_transaction(user[0], -300, "Еда", "2025-05-14", "Обед")
print("✅ Добавлены транзакции")

# Баланс
balance = db.get_balance(user[0])
print(f"💰 Баланс: {balance} ₽")

db.close()