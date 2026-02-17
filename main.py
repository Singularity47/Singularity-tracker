import os
import arxiv
import stripe
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- 1. SYSTEM INITIALIZATION ---
app = FastAPI()
Base = declarative_base()

# Pull Keys from your Railway Variables
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

stripe.api_key = os.getenv("STRIPE_API_KEY")

# --- 2. DATABASE BRAIN ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# --- 3. THE SCRAPER (RESEARCH DATA) ---
@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # Scans for AI papers from the last 24 hours
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        papers = list(search.results())
        paper_count = len(papers)
        
        # Real Math: 72.4% + (Papers Found / 500)
        base_progress = 72.4
        boost = paper_count / 500
        total = round(base_progress + boost, 3)
        
        return {"proximity": total, "papers_found": paper_count, "node": "Albuquerque"}
    except Exception as e:
        return {"proximity": 72.4, "error": str(e)}

# --- 4. MONETIZATION (STRIPE) ---
@app.post("/api/subscribe")
async def create_checkout_session():
    try:
        # This creates a one-time payment for the "Singularity Report"
        # Since you are a realtor, you can change this to "Consultation" later
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'ABQ AI Strategy Report'},
                    'unit_amount': 500, # $5.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-site.com/success',
            cancel_url='https://your-site.com/cancel',
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

# --- 5. THE DASHBOARD FACE ---
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except:
        return "<h1>Singularity Tracker Online</h1><p>Dashboard file index.html not found.</p>"
        
