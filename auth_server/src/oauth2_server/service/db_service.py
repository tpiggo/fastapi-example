from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session

_engine = create_engine(
    "postgresql://postgres:secret@127.0.0.1:5433/auth_server",
)


def db_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(db_session)]
