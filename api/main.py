from models import Base, engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import files, users, roles
import os

# Load demo data if in test or development environment
if os.getenv("ENV") in ['test', 'development']:
    import demo_data

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Marketease", description="Marketease API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
app.include_router(roles.router)
app.include_router(users.router)


@app.get("/app")
async def read_main():
    return {"message": "Hello World"}
