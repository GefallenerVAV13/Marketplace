from fastapi import FastAPI
from app.api.v1.categories import router as categories_router

app = FastAPI(title="Marketplace API", version="1.0.0")

app.include_router(categories_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Marketplace API"}


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "OK"}