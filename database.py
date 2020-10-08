from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

migrate = Migrate()
db = SQLAlchemy()


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    configure_database(app)

def create_engine():
    from sqlalchemy import create_engine
    from config import Config
    
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
    
    return engine