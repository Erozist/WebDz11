from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.database.db import get_db
from src.schemas.schemas import ContactCreate, ContactUpdate, Contact as ContactSchema
import src.repository.contacts as crud

router = APIRouter()

@router.post("/", response_model=ContactSchema)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(db=db, contact=contact)

@router.get("/", response_model=List[ContactSchema])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db=db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=ContactSchema)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=ContactSchema)
async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=ContactSchema)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search/", response_model=List[ContactSchema])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(db=db, query=query)

@router.get("/upcoming-birthdays/", response_model=List[ContactSchema])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_birthdays(db=db)
