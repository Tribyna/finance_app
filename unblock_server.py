from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from database.db_manager import DatabaseManager

class UnblockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/unblock":
            params = parse_qs(parsed.query)
            token = params.get("token", [None])[0]
            
            if token:
                db = DatabaseManager("finance.db")
                success = db.unblock_user_by_token(token)
                db.close()
                
                if success:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("""
                    <html>
                    <body style="font-family: Arial; text-align: center; padding: 50px;">
                        <h2 style="color: green;">Аккаунт разблокирован!</h2>
                        <p>Теперь вы можете войти в приложение.</p>
                        <button onclick="window.close()">Закрыть окно</button>
                    </body>
                    </html>
                    """.encode('utf-8'))
                    return
            
            self.send_response(400)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("""
            <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h2 style="color: red;">Неверный или просроченный токен</h2>
                <p>Запросите разблокировку заново, выполнив ещё 3 неудачные попытки входа.</p>
            </body>
            </html>
            """.encode('utf-8'))
            return
        
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"404 Not Found")

def run_server():
    server = HTTPServer(("localhost", 8000), UnblockHandler)
    print("Server running on http://localhost:8000")
    print("Click the link from email to unblock")
    server.serve_forever()

if __name__ == "__main__":
    run_server()