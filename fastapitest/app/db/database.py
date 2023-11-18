from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@ip:port/db?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:111111@127.0.0.1:3306/mydatabase?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

db = None


def get_db():
    global db
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
