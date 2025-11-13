# database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Use environment variables - IMPORTANT: Match Vercel environment variable names
DATABASE_URL = os.getenv(
    "DATABASE_URL",  # Changed to match Vercel's default
    os.getenv(
        "DATABASE_POSTGRES_URL",  # Fallback to your custom name
        "postgresql://postgres:1234@localhost:5432/dicebank"  # Final fallback for local dev
    )
)

class Base(DeclarativeBase):
    pass

# Better environment detection for production
environment = os.getenv("ENVIRONMENT", "development")
is_production = environment == "production"

engine = create_engine(
    DATABASE_URL,
    echo=not is_production,  # Only echo in non-production
    pool_pre_ping=True,
    pool_recycle=300,
    # Additional production settings
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
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
    if not is_production:  # Be careful with auto-creating tables in production
        Base.metadata.create_all(bind=engine)

def migrate_schema():
    if not is_production:  # Don't auto-migrate in production
        inspector = inspect(engine)
        with engine.connect() as conn:
            tables = inspector.get_table_names()
            if "support_replies" in tables:
                cols = [c["name"] for c in inspector.get_columns("support_replies")]
                if "message" not in cols:
                    conn.execute(text("ALTER TABLE support_replies ADD COLUMN message TEXT"))
                    conn.commit()