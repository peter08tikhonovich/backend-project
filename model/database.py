from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URI = 'sqlite:///./db.sql'

engine = create_engine(SQLALCHEMY_DB_URI)
DBSession = sessionmaker(engine, autoflush=False)