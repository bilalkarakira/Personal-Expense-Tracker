from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_async_session
import logging
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

Base  = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id  = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

class Expense(Base):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    
    


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)

async def create_db_and_tables():
    from backend.database import engine
    
    async with engine.begin() as conn:
        try:
            logger.info("Dropping all tables...")
            await conn.run_sync(Base.metadata.drop_all)
            
            logger.info("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
            
            # Verify tables were created
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = [row[0] for row in result]
            logger.info(f"Existing tables in database: {tables}")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
            raise