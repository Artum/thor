__all__ = ["register_routes"]


def register_routes(app):
    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/user')

    from .document import document_blueprint
    app.register_blueprint(document_blueprint, url_prefix='/api/document')