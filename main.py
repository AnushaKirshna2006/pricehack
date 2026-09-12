import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search

app = FastAPI(title="PriceHack API", description="Stateless Backend for PriceHack SaaS")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to PriceHack API (Stateless)"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
