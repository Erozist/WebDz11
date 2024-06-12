from fastapi import FastAPI
from src.database.db import engine, Base
from src.routes import contacts

app = FastAPI()

# Створення таблиць
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
