"""
главный файл приложения FastAPI
"""
from fastapi import FastAPI

from app.organizations.routers import router as organizations_router

app = FastAPI()

app.include_router(organizations_router)

