"""App configuration."""
import os


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = 'ch@ng3+h!$2sum+h!ngl8r!'

    # Static Assets
    STATIC_FOLDER = f'{os.getcwd()}/app/static/'
    TEMPLATES_FOLDER = f'{os.getcwd()}/app/templates/'
