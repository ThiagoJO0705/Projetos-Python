import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_DIR = os.path.join(BASE_DIR, 'database')

DB_PATH = os.path.join(DB_DIR, 'database.db')

db = create_engine(f'sqlite:///{DB_PATH}')

Base = declarative_base()

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session() 
        yield session
    finally:
        session.close()