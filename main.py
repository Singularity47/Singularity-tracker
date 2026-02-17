import os
import arxiv
import requests
import stripe
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# --- 1. CONFIGURATION ---
stripe.api_key = os.getenv("STRIPE_API_KEY")
NEWS_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = f"https://{os.getenv('RAILWAY_PUBLIC_DOMAIN')}" if os.getenv('RAILWAY_PUBLIC_DOMAIN') else "http://localhost:8000"

@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        res_count = len(list(search.results()))
        
        headlines = ["Synchronizing Global Feed..."]
        if NEWS_KEY:
            url = f"https://newsapi.org/v2/everything?q=Artificial%20Intelligence&apiKey={NEWS_KEY}"
            r = requests.get(url).json()
            articles = r.get('articles', [])[:5]
            if articles:
                headlines = [a.get('title', 'Headline Unavailable') for a in articles]

        # The Scientific AGI Math
        base = 71.0
        live_boost = ( (res_count/500)*0.3 + 0.65 ) * 10
        total = round(base + live_boost, 3)
        
        return {
            "proximity": total,
            "headlines": headlines,
            "papers": res_count,
            "node": "Albuquerque Node 01"
        }
    except Exception as e:
        return {"proximity": 72.4, "headlines": ["Feed Offline"], "error": str(e)}

@app.post("/api/subscribe")
async def create_pay_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'ABQ Node Deep Dive'}, 'unit_amount': 500}, 'quantity': 1}],
            mode='payment',
            success_url=f"{BASE_URL}/?unlocked=true", # AUTO-UNLOCK TRIGGER
            cancel_url=f"{BASE_URL}/",
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()
        
