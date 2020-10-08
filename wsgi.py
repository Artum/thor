from config import Config
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.WSGI_HOST, port=Config.WSGI_PORT)