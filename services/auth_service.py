import bcrypt
from services.email_service import EmailService

class AuthService:
    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def register(db, username, password, email):
        """Регистрация с email"""
        if db.get_user(username):
            return (None, None, "Пользователь уже существует")
        
        if db.get_user_by_email(email):
            return (None, None, "Email уже используется")
        
        if db.create_user(username, password, email):
            user = db.get_user(username)
            return (user[0], user[1], "OK")
        return (None, None, "Ошибка регистрации")
    
    @staticmethod
    def login(db, username, password):
        """Вход с проверкой блокировки и подсчётом попыток"""
        user = db.get_user(username)
        if not user:
            return (None, None, "Неверное имя или пароль")
        

        user_id = user[0]
        user_name = user[1]
        hashed = user[2]
        email = user[3]
        is_blocked = user[4] if len(user) > 4 else 0
        
        if is_blocked:
            return (None, None, "Аккаунт заблокирован!\nПроверьте почту для разблокировки.")
        
        if AuthService.verify_password(password, hashed):
            db.clear_failed_attempts(user_id)
            return (user_id, user_name, "OK")
        
        db.add_failed_attempt(user_id)
        failed_count = db.get_failed_attempts_count(user_id)
        
        if failed_count >= 3:
            db.block_user(user_id)
            if email:
                token = EmailService.generate_unblock_token()
                db.save_unblock_token(user_id, token)
                EmailService.send_block_notification(email, user_name, token)
            return (None, None, "Аккаунт заблокирован!\nПроверьте почту для разблокировки.")
        
        remaining = 3 - failed_count
        return (None, None, f"Неверный пароль. Осталось попыток: {remaining}")