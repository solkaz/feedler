"""
Define how to get a DB session. Used by FastAPI.
"""

from collections.abc import AsyncGenerator

from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from feedler.settings import settings


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Getter
    """
    engine = create_async_engine(settings.pg_url)
    factory = async_sessionmaker(engine)

    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise error
