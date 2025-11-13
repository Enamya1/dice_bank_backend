from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@localhost:5432/dicebank")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() in ("1", "true", "yes", "on")



class Base(DeclarativeBase):
    pass



engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


def migrate_schema():
    inspector = inspect(engine)
    with engine.connect() as conn:
        tables = inspector.get_table_names()
        if "support_replies" in tables:
            cols = [c["name"] for c in inspector.get_columns("support_replies")]
            if "message" not in cols:
                conn.execute(text("ALTER TABLE support_replies ADD COLUMN message TEXT"))
                conn.commit()
