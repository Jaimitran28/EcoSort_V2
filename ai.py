# ai.py
import google.generativeai as genai
import re
from keywords import keyword_map

# --- Configure Gemini API ---
API_KEY = "AIzaSyAAQE852yk3wBugXD7zU-hrwv9ED3gxcxU"
genai.configure(api_key=API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# Predefined tips for known categories
PREDEFINED_TIPS = {
    "recyclable": [
        "Rinse before recycling.",
        "Separate caps and lids.",
        "Do not mix with trash."
    ],
    "compostable": [
        "Add to compost bin.",
        "Avoid meat and dairy.",
        "Chop large scraps."
    ],
    "hazardous": [
        "Handle with gloves.",
        "Dispose at a hazardous waste center.",
        "Do not mix with regular trash."
    ],
    "trash": [
        "Dispose in trash bin.",
        "Do not burn.",
        "Keep in covered bin."
    ]
}


def parse_tips(raw_text: str, max_points: int = 3) -> list:
    """
    Parse Gemini response and return a clean list of numbered tips.
    """
    if not raw_text or raw_text.strip() == "":
        return []

    # Extract numbered points
    points = re.findall(r'\d+\.\s*(.+)', raw_text)
    if not points:
        # fallback: split by newlines or periods
        points = [line.strip() for line in re.split(r'\n|\.', raw_text) if line.strip()]

    return points[:max_points]


async def generate_disposal_tips(item_name: str, category: str = None) -> list:
    """
    Generate disposal/reuse tips.
    Uses predefined tips if category is known, otherwise calls Gemini.
    Returns a list of max 3 tips.
    """

    # --- Validate item ---
    if not item_name or item_name.strip().lower() in ["unknown", "unsure", "none", ""]:
        return ["Please enter a proper waste item to get disposal tips."]

    # --- Determine category if not provided ---
    if not category or category == "unknown":
        item_lower = item_name.lower()
        category = "unknown"
        for keyword, cat in keyword_map.items():
            if keyword in item_lower:
                category = cat
                break

    # --- Return predefined tips for known categories ---
    if category in PREDEFINED_TIPS:
        return PREDEFINED_TIPS[category]

    # --- Otherwise, ask Gemini ---
    try:
        prompt = f"""
        You are an eco-assistant. Provide a very short, clear, and practical numbered list
        of 3 tips for disposing or reusing the following waste item:

        Waste item: "{item_name}"
        Category: {category}

        Only provide numbered tips, nothing else.
        """

        response = model.generate_content(prompt)
        raw_tips = response.text if response and response.text else ""
        tips = parse_tips(raw_tips)

        # Fallback if Gemini returns nothing
        if not tips:
            tips = ["Dispose properly according to local rules."]

        return tips

    except Exception as e:
        return [f"Error generating tips: {e}"]
