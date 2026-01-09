import os
from flask import Flask
from .config import Config
from .extensions.db import db
from .extensions.error_handling import register_handlers
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Register blueprints
    from .api.v2.users.views import users_bp
    from .api.v2.books.views import books_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(books_bp)

    # Register web routes
    from .routes import register_routes

    register_routes(app)

    # Error handlers
    register_handlers(app)

    return app
