from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_PORT = os.environ.get("DB_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://"
    f"{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}"
    f"@db:{DB_PORT}/{POSTGRES_DB}"
    # f"@0.0.0.0:{DB_PORT}/{POSTGRES_DB}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
