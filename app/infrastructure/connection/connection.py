import logging

from urllib.parse import quote
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def build_pg_conninfo(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
) -> str:
    conninfo = (
        f"postgresql://{quote(user, safe='')}:{quote(password, safe='')}"
        f"@{host}:{port}/{db_name}"
    )
    logger.debug(f"Building PostgreSQL connection string (password omitted): "
                 f"postgresql://{quote(user, safe='')}@{host}:{port}/{db_name}")
    return conninfo

def get_session(
        db_name: str,
        host: str,
        port: int,
        user: str,
        password: str,
):
    engine = create_engine(
        build_pg_conninfo(
            db_name=db_name,
            host=host,
            port=port,
            user=user,
            password=password
        ),
        echo=True,
    )
    
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    
    return SessionLocal()



    