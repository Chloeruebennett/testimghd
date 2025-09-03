import databases
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base

database = databases.Database(settings.SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
