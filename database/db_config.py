from os import getenv

from dotenv import load_dotenv


load_dotenv()


class DatabaseConfig:
    """Database configuration class.
    Imports database settings from .env file."""
    config = {'user': getenv('DATABASE_USER'),
              'password': getenv('DATABASE_PASSWORD'),
              'database': getenv('DATABASE_NAME'),
              'host': getenv('DATABASE_HOST'),
              'port': getenv('DATABASE_PORT')}
