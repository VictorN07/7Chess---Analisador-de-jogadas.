from fastapi import FastAPI
from routers import partidas
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="7Chess Analyzer API",
    description="This API is for analyzing chess games",
    version="0.1.0"
)

app.include_router(partidas.router)

@app.get("/")
def home():
    return {"status": "API is running", "message": "Welcome to the 7Chess Analyzer API!"}

