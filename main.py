import os
import arxiv
import requests
import stripe
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # 1. Research (arXiv) - 30% Weight
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        papers = list(search.results())
        res_score = (len(papers) / 500) * 0.3

        # 2. News Feed (NewsAPI) - 10% Weight
        news_key = os.getenv("NEWS_API_KEY")
        headlines = ["System Syncing..."]
        if news_key:
            url = f"https://newsapi.org/v2/everything?q=Artificial%20Intelligence&apiKey={news_key}"
            news_data = requests.get(url).json()
            headlines = [art['title'] for art in news_data.get('articles', [])[:5]]

        # 3. Development/Economy/Energy - 60% Weight (Placeholders)
        # These represent the other 6 power systems
        dev_score = 0.25 
        energy_score = 0.18
        market_score = 0.12

        # THE TRUE MATH CALCULATION
        base = 71.8
        live_boost = res_score + dev_score + energy_score + market_score
        total = round(base + live_boost, 3)
        
        return {
            "proximity": total,
            "headlines": headlines,
            "papers": len(papers),
            "node": "Albuquerque Node 01"
        }
    except Exception as e:
        return {"proximity": 72.4, "headlines": ["Feed Offline"], "error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except:
        return "<h1>Node Online</h1><p>Index.html missing.</p>"
        
