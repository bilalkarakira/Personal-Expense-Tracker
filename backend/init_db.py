import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from backend.database import DATABASE_URL
from backend.auth.models import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    logger.info(f"Connecting to: {DATABASE_URL}")
    engine = create_async_engine(DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        # Verify current connection
        result = await conn.execute(text("SELECT current_database();"))
        db_name = result.scalar()
        logger.info(f"Connected to database: {db_name}")
        
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        # Verify tables
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
        tables = [row[0] for row in result]
        logger.info(f"Created tables: {tables}")

if __name__ == "__main__":
    asyncio.run(init_db())