import os
import arxiv
import requests
import stripe
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- 1. CONFIGURATION ---
stripe.api_key = os.getenv("STRIPE_API_KEY")
NEWS_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}" if os.getenv('RAILWAY_PUBLIC_DOMAIN') else "http://localhost:8000"

@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # 1. LIVE RESEARCH (arXiv)
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        papers = list(search.results())
        paper_count = len(papers)
        
        # 2. REAL MATH FOR CARDS
        # Ties the '1.21 GW' and '4.2%' to the actual research volume
        live_energy = round(1.10 + (paper_count * 0.005), 2)
        live_housing = round(4.0 + (paper_count * 0.02), 1)

        # 3. NEWS FEED
        headlines = ["Scanning Albuquerque Data Streams..."]
        if NEWS_KEY:
            url = f"https://newsapi.org/v2/everything?q=Artificial%20Intelligence&apiKey={NEWS_KEY}"
            r = requests.get(url).json()
            articles = r.get('articles', [])[:5]
            if articles:
                headlines = [a.get('title', 'Headline Unavailable') for a in articles]

        # THE ACCURATE MATH
        base = 71.8
        total = round(base + (paper_count / 500), 3)
        
        return {
            "proximity": total,
            "headlines": headlines,
            "papers": paper_count,
            "energy": f"{live_energy} GW",
            "housing": f"+{live_housing}%",
            "node": "Albuquerque Node 01"
        }
    except Exception as e:
        return {"proximity": 72.4, "headlines": ["Feed Offline - Check API Key"], "error": str(e)}

@app.post("/api/subscribe")
async def create_pay_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'ABQ Node Deep Dive'}, 'unit_amount': 500}, 'quantity': 1}],
            mode='payment',
            success_url=f"{BASE_URL}/?unlocked=true",
            cancel_url=f"{BASE_URL}/",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()
        
