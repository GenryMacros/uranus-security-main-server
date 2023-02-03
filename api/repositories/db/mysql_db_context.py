import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


class AppDBConf:
    __LOGIN = "API"
    __PASSWORD = "renek1"
    __HOST = "localhost"
    __PORT = "1433"
    __DB_NAME = "Uranus_Security"
    __DRIVER = "ODBC+DRIVER+18+for+SQL+Server"
    __CONNECTION_STRING = f"mssql+pyodbc://{__LOGIN}:{__PASSWORD}" \
                          f"!@{__HOST}:{__PORT}/" \
                          f"{__DB_NAME}?driver={__DRIVER}&TrustServerCertificate=YES&Trusted_Connection=YES"
    __ENGINE = db.create_engine(__CONNECTION_STRING)
    DB_SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=__ENGINE))
    BASE = declarative_base()
    BASE.query = DB_SESSION.query_property()

