from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config.settings import get_settings

# engine que vamos a conectarnos a la base de datos
engine = create_async_engine(get_settings().database_url)

# Factory de sesiones locales que vamos a usar per-request
AsyncLocalSession = async_sessionmaker(engine)
