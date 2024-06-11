from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Contact
from schemas import ContactCreate, ContactUpdate
from datetime import date, timedelta

async def get_contact(db: AsyncSession, contact_id: int):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalars().first()

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()

async def create_contact(db: AsyncSession, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)
    return db_contact

async def update_contact(db: AsyncSession, contact_id: int, contact: ContactUpdate):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        await db.commit()
        await db.refresh(db_contact)
        return db_contact
    return None

async def delete_contact(db: AsyncSession, contact_id: int):
    db_contact = await get_contact(db, contact_id)
    if db_contact:
        await db.delete(db_contact)
        await db.commit()
        return db_contact
    return None

async def search_contacts(db: AsyncSession, query: str):
    result = await db.execute(
        select(Contact).where(
            (Contact.first_name.ilike(f"%{query}%")) |
            (Contact.last_name.ilike(f"%{query}%")) |
            (Contact.email.ilike(f"%{query}%"))
        )
    )
    return result.scalars().all()

async def get_upcoming_birthdays(db: AsyncSession):
    today = date.today()
    next_week = today + timedelta(days=7)
    result = await db.execute(
        select(Contact).where(
            (Contact.birthday >= today) & (Contact.birthday <= next_week)
        )
    )
    return result.scalars().all()
