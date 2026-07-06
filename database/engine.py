from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event
from database.models import Base

engine = create_engine("sqlite:///musculation.db")
@event.listens_for(engine, "connect")
def _enable_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()

def init_db():
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(engine)