from fastapi import FastAPI, HTTPException
from database import connect_to_mongo
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from scrapeModule.service import ArchitectureScraper
from scrapeModule.model import Architecture

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = connect_to_mongo()
scraper = ArchitectureScraper(db)

@app.get("/")
def read_root():
    return {"message": "Welcome to AWS Architecture Scraper API!"}

@app.post("/scrape")
async def scrape_architecture(url: str):
    try:
        architecture = await scraper.scrape_and_store(url)
        return {"message": "Architecture scraped successfully", "data": architecture.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/architectures", response_model=List[Architecture])
async def get_architectures(skip: int = 0, limit: int = 100):
    try:
        architectures = await scraper.get_architectures(skip=skip, limit=limit)
        return architectures
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))