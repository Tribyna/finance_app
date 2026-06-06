import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

class EmailService:
    SMTP_SERVER = "smtp.mail.ru"
    SMTP_PORT = 587
    SENDER_EMAIL = "finance_app@mail.ru"  
    SENDER_PASSWORD = "AamYZZBv41UN6KrM5E5I" 

    @staticmethod
    def generate_unblock_token():
        return secrets.token_urlsafe(32)

    @staticmethod
    def send_block_notification(recipient_email, username, token):
        subject = "🔐 Ваш аккаунт заблокирован - Личные финансы"
        unblock_link = f"http://localhost:8000/unblock?token={token}"
        
        html_body = f"""<html>
        <body>
            <h2>⚠️ Ваш аккаунт заблокирован</h2>
            <p>Было совершено 3 неудачных попытки входа в аккаунт <b>{username}</b>.</p>
            <p><b>Доступ к аккаунту заблокирован до вашего вмешательства.</b></p>
            <p>Нажмите кнопку ниже, чтобы разблокировать доступ:</p>
            <a href="{unblock_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">🔓 Разблокировать аккаунт</a>
            <p>Если это были не вы, разблокируйте аккаунт и смените пароль.</p>
            <hr>
            <small>Приложение "Личные финансы"</small>
        </body>
        </html>"""
        
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = EmailService.SENDER_EMAIL
        msg["To"] = recipient_email
        msg.attach(MIMEText(html_body, "html"))
        
        try:
            with smtplib.SMTP(EmailService.SMTP_SERVER, EmailService.SMTP_PORT, timeout=30) as server:
                server.starttls()
                server.login(EmailService.SENDER_EMAIL, EmailService.SENDER_PASSWORD)
                server.send_message(msg)
            print(f"✅ Письмо отправлено на {recipient_email}")
            return True
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")
            return False