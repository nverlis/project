import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_url = os.getenv("DB_URL")
db_port = os.getenv("DB_PORT")
db_root_base = os.getenv("DB_NAME", "homeworks")

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}:{db_port}/{db_root_base}",
    pool_recycle=3600
)

session_homeworks = Session(bind=engine)

df = pd.read_parquet(r"/converted_data.parquet")

df.to_sql(
    name="vibe",
    con=engine,
    schema="public",
    if_exists="replace",
    index=False,
)

