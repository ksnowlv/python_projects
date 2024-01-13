from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = None

Base = declarative_base()



def get_db():
    global db
    return db
    # global db
    # try:
    #     db = SessionLocal()
    #     yield db
    # finally:
    #     db.close()


def init_db(mysql_url):
    engine = create_engine(
        mysql_url
    )

    Base.metadata.create_all(bind=engine)

    global db
    try:
        db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        yield db
    finally:
        db.close()
