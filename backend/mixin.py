from typing import TypeVar, Generic, Type, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi import HTTPException
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDMixin(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, limit: int = 100) -> List[ModelType]:
        query = select(self.model).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, db: AsyncSession, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, id: int, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = await self.get(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        obj_in_data = obj_in.dict()
        for field, value in obj_in_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> ModelType:
        db_obj = await self.get(db, id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Object not found")
        await db.delete(db_obj)
        await db.commit()
        return db_obj