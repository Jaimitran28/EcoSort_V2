# app.py
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from classifier import classify_image
from rules import keyword_map, FACTS
import os
from ai import generate_disposal_tips
import random

app = FastAPI()

# Mount static files folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Home route
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main web page with a random 'Did You Know?' fact.
    """
    fact = random.choice(FACTS)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "fact_short": fact["short"],
            "fact_detail": fact["detail"],
        }
    )

# API endpoint for facts
@app.get("/fact")
async def get_fact():
    """Return a random 'Did You Know?' fact."""
    try:
        fact = random.choice(FACTS)
        return JSONResponse(fact)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# API endpoint for image upload and classification
@app.post("/predict_image")
async def predict_image(image: UploadFile = File(...)):
    """
    Handle image upload -> classify -> generate Gemini disposal tips.
    """
    try:
        # Run classifier
        result = await classify_image(image.file)
        category = result.get("category", "unknown")
        top_labels = result.get("top_labels", [])

        # Use the top label or fallback to "waste item"
        item_name = top_labels[0] if top_labels else "waste item"

        # --- Ask Gemini for disposal tips ---
        tips = await generate_disposal_tips(item_name, category)

        return JSONResponse({
            "source": "image",
            "category": category,
            "confidence": result.get("confidence", 0),
            "top_labels": top_labels,
            "tips": tips
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# API endpoint for text input and classification
@app.post("/predict_text")
async def predict_text(data: dict):
    """
    Handle user-entered text (waste description) -> classify -> generate Gemini disposal tips.
    """
    try:
        if not data or "text" not in data:
            return JSONResponse({"error": "No text provided"}, status_code=400)

        text_input = data["text"].lower()
        category = "unknown"

        # Match category using keyword map
        for keyword, cat in keyword_map.items():
            if keyword in text_input:
                category = cat
                break

        if category == "unknown":
            tips = ["Please enter a proper waste item to get disposal tips."]
            confidence = 0
            top_labels = []
        else:
            tips = await generate_disposal_tips(text_input, category)
            confidence = 1.0
            top_labels = [text_input]



        confidence = 1.0 if category != "unknown" else 0

        return JSONResponse({
            "source": "text",
            "category": category,
            "confidence": confidence,
            "top_labels": [text_input] if category != "unknown" else [],
            "tips": tips
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

# Run the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
