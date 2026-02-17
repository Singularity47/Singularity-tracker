import os
import arxiv
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # 1. Research (arXiv) - 30% Weight
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        res_score = (len(list(search.results())) / 500) * 0.3

        # 2. News/Sentiment (NewsAPI) - 10% Weight
        # We'll fetch headlines to show, but also use them for the "buzz" score
        news_key = os.getenv("NEWS_API_KEY")
        news_url = f"https://newsapi.org/v2/everything?q=Artificial%20Intelligence&apiKey={news_key}"
        news_data = requests.get(news_url).json()
        headlines = [art['title'] for art in news_data.get('articles', [])[:5]]
        news_score = 0.05 # Placeholder for sentiment analysis

        # 3. Development/Energy/Economy - 60% Weight (Placeholders for now)
        dev_score = 0.25 
        energy_score = 0.18
        market_score = 0.12

        # THE TOTAL CALCULATION
        base = 71.8
        live_boost = res_score + news_score + dev_score + energy_score + market_score
        total = round(base + live_boost, 3)
        
        return {
            "proximity": total,
            "headlines": headlines,
            "node": "Albuquerque Node 01"
        }
    except Exception as e:
        return {"proximity": 72.4, "headlines": ["System Syncing..."], "error": str(e)}

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()
        
