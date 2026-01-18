import re
from itinerary_llm import generate_itinerary


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
    # ✅ STATE IS NOW LOCAL (THIS FIXES EVERYTHING)
    conversation_state = {
        "destination": None,
        "days": None,
        "travel_style": None,
        "budget_type": None,
        "complete": False
    }

    def chatbot(payload: dict):
        text = payload["message"].strip().lower()

        # 🧠 Destination
        if not conversation_state["destination"]:
            if looks_like_destination(text):
                conversation_state["destination"] = payload["message"].title()
                return {"reply": "💫 Great choice! How many days is your trip?"}
            return {"reply": "✈️ Where would you like to travel?"}

        # 🧠 Days
        if not conversation_state["days"]:
            days = extract_days(text)
            if days:
                conversation_state["days"] = days
                return {"reply": "🧳 Nice! What is your travel style? (solo, family, couple)"}
            return {"reply": "Please tell me the trip duration (e.g. 5 days)"}

        # 🧠 Travel style
        if not conversation_state["travel_style"]:
            style = extract_travel_style(text)
            if style:
                conversation_state["travel_style"] = style
                return {"reply": "💰 Is this a budget, mid-range, or luxury trip?"}
            return {"reply": "Please choose a travel style: solo, family, or couple"}

        # 🧠 Budget
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

        # 🔁 Follow-ups
        if "food" in text:
            return {
                "reply": f"""
🍽 Food Recommendations in {conversation_state['destination']}

• Local street food & night markets  
• Authentic regional dishes  
• Popular local restaurants  

Would you like hotels or activities next? 😊
""".strip()
            }

        if "hotel" in text:
            return {
                "reply": f"""
🏨 Hotel Suggestions ({conversation_state['budget_type'].title()})

• Centrally located stays  
• Good reviews  
• Suitable for {conversation_state['travel_style']} travelers  

Want food or activities next?
""".strip()
            }

        if "activity" in text or "activities" in text:
            return {
                "reply": f"""
🎯 Top Activities in {conversation_state['destination']}

• Sightseeing  
• Cultural experiences  
• Leisure & relaxation  

Would you like food or hotels next?
""".strip()
            }

        return {
            "reply": "I can help with food 🍽, hotels 🏨, or activities 🎯. What would you like?"
        }

    return chatbot
