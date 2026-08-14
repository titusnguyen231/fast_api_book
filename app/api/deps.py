from typing import Generator
from app.db.sessions import sessionLocal

def get_db() -> Generator:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()