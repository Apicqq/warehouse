import os

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import settings

load_dotenv()


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(
    cls=PreBase,
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    ),
)
if os.getenv("TESTING") == "True":
    engine = create_async_engine(settings.sqlite_db_url)
else:
    engine = create_async_engine(settings.postgres_db_url)
AsyncSessionLocal = async_sessionmaker(engine)


async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
