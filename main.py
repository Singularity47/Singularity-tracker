@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # 1. Research Metric (arXiv)
        search = arxiv.Search(query="cat:cs.AI", max_results=50)
        res_score = len(list(search.results())) / 500 

        # 2. Infrastructure Metric (EIA Placeholder)
        # In ABQ, we track the power grid load
        energy_score = 0.15 # Represents current global GPU power draw

        # 3. Code Metric (GitHub Placeholder)
        # Tracking commits to major AI repos
        code_score = 0.22 

        # 4. Economic Metric (Stripe/Market)
        # Every dollar through your node increases adoption
        market_score = 0.12

        # THE TOTAL CALCULATION
        base = 71.0
        live_boost = res_score + energy_score + code_score + market_score
        total = round(base + live_boost, 3)
        
        return {
            "proximity": total,
            "breakdown": {
                "research": res_score,
                "energy": energy_score,
                "dev_velocity": code_score,
                "market": market_score
            },
            "node": "Albuquerque"
        }
    except Exception as e:
        return {"proximity": 72.4, "error": str(e)}
        
