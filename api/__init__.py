__all__ = ["register_routes"]


def register_routes(app):
    from .users import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/users')