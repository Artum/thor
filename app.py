from flask import Flask

from config import Config
from api import register_routes
from database import init_db
from auth import init_auth

__all__ = ["create_app"]


def create_app():
    app = Flask("Thor", static_folder=None)
    app.config.from_object(Config)
    
    with app.app_context():
        init_db(app)
        init_auth(app)
        register_routes(app)
    
    return app
