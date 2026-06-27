from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///Database/RMSDB.db",echo=False)

LocalSession = sessionmaker(bind = engine)


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()