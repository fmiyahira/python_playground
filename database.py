from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://username:password@db:5432/playground"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session