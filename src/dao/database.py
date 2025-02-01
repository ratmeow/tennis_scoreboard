import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.config import settings
from src.utils.exceptions import DatabaseInternalError

logger = logging.getLogger(__name__)
engine = create_engine(url=settings.DB_URL)
session_maker = sessionmaker(engine, expire_on_commit=False)


def connection(commit: bool = False):
    def decorator(method):
        def wrapper(*args, **kwargs):
            with session_maker() as session:
                try:
                    result = method(*args, session=session, **kwargs)
                    if commit:
                        session.commit()
                    return result
                except Exception as e:
                    session.rollback()
                    logger.error(e)
                    raise DatabaseInternalError
                finally:
                    session.close()

        return wrapper

    return decorator


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
