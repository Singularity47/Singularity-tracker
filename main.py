from fastapi.responses import HTMLResponse
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = FastAPI()

# --- 1. Database Setup (The Brain) ---
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix for Railway's URL format (SQLAlchemy needs 'postgresql', not 'postgres')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connect to the Database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create the Table to store Data
class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)  # e.g., "GitHub", "EIA"
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Build the database tables
Base.metadata.create_all(bind=engine)

# --- 2. The API Endpoints (The 8-Power System) ---

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/api/github-activity")
def github_status():
    # Placeholder for live GitHub tracking
    return {"source": "GitHub", "status": "Tracking repo velocity"}

@app.get("/api/energy")
def energy_status():
    # Placeholder for EIA tracking
    return {"source": "EIA", "status": "Tracking data center power"}

@app.get("/api/models")
def model_status():
    # Placeholder for Hugging Face tracking
    return {"source": "Hugging Face", "status": "Tracking model count"}

@app.get("/api/news")
def news_status():
    return {"source": "NewsAPI", "status": "Tracking AI headlines"}

@app.get("/api/finance")
def finance_status():
    return {"source": "Stripe", "status": "Payment gateway active"}
        
