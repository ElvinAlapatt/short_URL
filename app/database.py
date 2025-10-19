from sqlmodel import SQLModel , create_engine , Session
from .config import settings
DATABASE_URL = f"postgresql://{settings.DATABASE_USER_NAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"

engine = create_engine(DATABASE_URL,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session