import bcrypt

class AuthService:
    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @staticmethod
    def register(db, username, password):
        if db.get_user(username):
            return (None, None)
        # Передаём простой пароль, хеширование внутри db.create_user
        if db.create_user(username, password):
            user = db.get_user(username)
            return (user[0], user[1])
        return (None, None)
    
    @staticmethod
    def login(db, username, password):
        user = db.get_user(username)
        if user and AuthService.verify_password(password, user[2]):
            return (user[0], user[1])
        return (None, None)