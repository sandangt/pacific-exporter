from typing import Tuple

from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker, Session

from app.constant import DB_FILE_PATH


def init_db_config() -> Tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(
        f'sqlite:///{DB_FILE_PATH}',
        connect_args={'check_same_thread': False}
    )
    return engine, sessionmaker(bind=engine, autocommit=False, autoflush=False)
