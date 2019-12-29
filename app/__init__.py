"""Initialize app."""
from flask import Flask


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object("config.Config")

    # Initialize Plugins

    return app
