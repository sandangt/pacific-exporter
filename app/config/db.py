from typing import Tuple

from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker, Session


def init_db_config() -> Tuple[Engine, sessionmaker[Session]]:
    engine = create_engine(
        'sqlite:///./.tmp/data.db',
        connect_args={'check_same_thread': False}
    )
    return engine, sessionmaker(bind=engine, autocommit=False, autofush=False)
