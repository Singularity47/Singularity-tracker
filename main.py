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

@app.get("/api/tracker-logic")
d@app.get("/api/tracker-logic")
def calculate_progress():
    try:
        # ... (Keep your existing math here) ...
        total = round(71.0 + live_boost, 3)
        
        # New: Pre-formatted text for Twitter/X sharing
        share_text = f"The Singularity is approaching. Node 01 (ABQ) reports AGI Proximity at {total}%! Track the metrics here:"
        
        return {
            "proximity": total,
            "headlines": headlines,
            "share_msg": share_text,
            "node": "Albuquerque Node 01"
        }
    except Exception as e:
        return {"proximity": 72.4, "share_msg": "Tracking the Singularity...", "error": str(e)}

# FIXED LINE: Changed @app.get with methods to @app.post
@app.post("/api/subscribe")
async def create_pay_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'ABQ Node Deep Dive Report'},
                    'unit_amount': 500,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://' + os.getenv('RAILWAY_PUBLIC_DOMAIN', 'your-node.up.railway.app') + '/success',
            cancel_url='https://' + os.getenv('RAILWAY_PUBLIC_DOMAIN', 'your-node.up.railway.app') + '/',
        )
        return {"url": session.url}
    except Exception as e:
        return {"error": str(e)}

@app.get("/success", response_class=HTMLResponse)
def payment_success():
    return """
    <body style="background: #000; color: #00ff41; font-family: monospace; text-align: center; padding: 50px;">
        <h1>[ ACCESS GRANTED ]</h1>
        <p>DEEP DIVE MODULE ACTIVATED FOR ALBUQUERQUE_01</p>
        <a href="/" style="color: #fff;">RETURN TO DASHBOARD</a>
    </body>
    """

@app.get("/", response_class=HTMLResponse)
def home():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except:
        return "<h1>Node Online</h1><p>Index.html missing. Check GitHub files.</p>"
        
