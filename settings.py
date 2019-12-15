import os

from dotenv import load_dotenv
load_dotenv()


POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME')
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

