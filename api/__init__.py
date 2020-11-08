__all__ = ["register_routes"]


def register_routes(app):
    from .users import users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/user')

    from .invoices import invoices_blueprint
    app.register_blueprint(invoices_blueprint, url_prefix='/api/invoice')