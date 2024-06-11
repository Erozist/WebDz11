from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import engine, Base, get_db
#from models import Contact
from schemas import ContactCreate, ContactUpdate, Contact as ContactSchema
import crud

app = FastAPI()

# Створення таблиць
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/contacts/", response_model=ContactSchema)
async def create_contact(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[ContactSchema])
async def read_contacts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_contacts(db=db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=ContactSchema)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=ContactSchema)
async def update_contact(contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=ContactSchema)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    db_contact = await crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=List[ContactSchema])
async def search_contacts(query: str, db: AsyncSession = Depends(get_db)):
    return await crud.search_contacts(db=db, query=query)

@app.get("/contacts/upcoming-birthdays/", response_model=List[ContactSchema])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await crud.get_upcoming_birthdays(db=db)
