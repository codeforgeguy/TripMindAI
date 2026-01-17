import re
from itinerary_llm import generate_itinerary

# 🔒 Simple in-memory conversation state
conversation_state = {
    "destination": None,
    "days": None,
    "travel_style": None,
    "budget_type": None,
    "complete": False
}


# --------- helpers ---------

def extract_days(text: str):
    match = re.search(r"(\d+)\s*(day|days)", text)
    if match:
        return int(match.group(1))
    if text.isdigit():
        return int(text)
    return None


def extract_travel_style(text: str):
    for style in ["solo", "family", "couple"]:
        if style in text:
            return style
    return None


def extract_budget(text: str):
    for budget in ["budget", "mid-range", "mid range", "luxury"]:
        if budget in text:
            return "mid-range" if "mid" in budget else budget
    return None


def looks_like_destination(text: str):
    return len(text.split()) <= 4 and not extract_days(text)


# --------- main engine ---------

def build_graph():

    def chatbot(payload: dict):
        text = payload["message"].strip().lower()

        # 🧠 Fill destination
        if not conversation_state["destination"]:
            if looks_like_destination(text):
                conversation_state["destination"] = payload["message"].title()
                return {"reply": "💫 Great choice! How many days is your trip?"}
            return {"reply": "✈️ Where would you like to travel?"}

        # 🧠 Fill days
        if not conversation_state["days"]:
            days = extract_days(text)
            if days:
                conversation_state["days"] = days
                return {"reply": "🧳Nice! What is your travel style? (solo, family, couple)"}
            return {"reply": "Please tell me the trip duration (e.g. 5 days)"}

        # 🧠 Fill travel style
        if not conversation_state["travel_style"]:
            style = extract_travel_style(text)
            if style:
                conversation_state["travel_style"] = style
                return {"reply": "💰 Is this a budget, mid-range, or luxury trip?"}
            return {"reply": "Please choose a travel style: solo, family, or couple"}

        # 🧠 Fill budget
        if not conversation_state["budget_type"]:
            budget = extract_budget(text)
            if budget:
                conversation_state["budget_type"] = budget
            else:
                return {"reply": "Please choose: budget, mid-range, or luxury"}

        # ✨ Generate itinerary ONCE
        if not conversation_state["complete"]:
            itinerary = generate_itinerary(conversation_state)
            conversation_state["complete"] = True
            return {
                "reply": itinerary,
                "complete": True
            }

        # 🔁 Follow-up intent handling
        if "food" in text:
            return {
                "reply": f"""
🍽 Food Recommendations in {conversation_state['destination']}

• Local street food & night markets  
• Authentic regional dishes  
• Mid-range & popular local restaurants  
• Café & dessert spots  

Would you like hotel or activities next? 😊
""".strip()
            }

        if "hotel" in text:
            return {
                "reply": f"""
🏨 Hotel Suggestions ({conversation_state['budget_type'].title()})

• Centrally located hotels  
• Comfortable stays with good reviews  
• Suitable for {conversation_state['travel_style']} travelers  

Want food or activities next?
""".strip()
            }

        if "activity" in text or "activities" in text:
            return {
                "reply": f"""
🎯 Top Activities in {conversation_state['destination']}

• City highlights & sightseeing  
• Adventure & nature experiences  
• Cultural & local experiences  
• Relaxation & leisure  

Would you like food or hotels next?
""".strip()
            }

        # fallback
        return {
            "reply": "I can help with food 🍽, hotels 🏨, or activities 🎯. What would you like?"
        }

    return chatbot
