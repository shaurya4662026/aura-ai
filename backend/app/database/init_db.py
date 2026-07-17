from app.database.database import Base, engine
from app.database.tables import UserTable

def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)