from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from db import (
    Base,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_DATABASE,
    engine,
)
import model


# Connect without selecting a DB, then create it if missing.
server_engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/"
)
with server_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`"))
    conn.commit()

Base.metadata.create_all(bind=engine)