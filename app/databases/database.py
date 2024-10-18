import os

from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = os.environ.get("")
DATABASE_URL = "YOUR-DATABASE-NAME"
sqlite_url = f"sqlite:///database.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
