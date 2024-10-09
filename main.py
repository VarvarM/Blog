from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Form, Request, HTTPException, Depends
from api import router as api_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(title='Blog')
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
