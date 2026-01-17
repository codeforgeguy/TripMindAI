from itinerary_llm import generate_itinerary
from utils import extract_days, extract_destination, extract_travel_style, extract_budget

conversation_state = {
    "destination": None,
    "days": None,
    "travel_style": None,
    "budget_type": None,
    "complete": False
}


def chat_engine(message: str):
    try:
        text = message.strip()

        # 🔍 Extract info freely
        destination = extract_destination(text)
        days = extract_days(text)
        travel_style = extract_travel_style(text)
        budget = extract_budget(text)

        if destination:
            conversation_state["destination"] = destination
        if days:
            conversation_state["days"] = days
        if travel_style:
            conversation_state["travel_style"] = travel_style
        if budget:
            conversation_state["budget_type"] = budget

        # ✅ Generate itinerary ONLY ONCE
        if (
            conversation_state["destination"]
            and conversation_state["days"]
            and conversation_state["travel_style"]
            and conversation_state["budget_type"]
            and not conversation_state["complete"]
        ):
            conversation_state["complete"] = True

            itinerary_text = generate_itinerary(conversation_state)

            # 🔒 Force string response
            return {
                "reply": str(itinerary_text),
                "complete": True
            }

        # 🧠 Ask only missing info
        missing = []
        if not conversation_state["destination"]:
            missing.append("where you want to travel")
        if not conversation_state["days"]:
            missing.append("how many days")
        if not conversation_state["travel_style"]:
            missing.append("your travel style (solo, family, couple)")
        if not conversation_state["budget_type"]:
            missing.append("your budget (budget, mid-range, luxury)")

        return {
            "reply": f"Got it 👍 Could you tell me {', '.join(missing)}?"
        }

    except Exception as e:
        print("❌ CHAT ENGINE ERROR:", e)
        return {
            "reply": "⚠️ Something went wrong while planning your trip. Please try again."
        }
    