import re

def normalize_message(text: str) -> dict:
    text = text.lower()

    destination = None
    days = None
    travel_style = None
    budget_type = None

    # Destination (basic — extend later)
    for place in ["bali", "goa", "paris", "china", "hong kong", "singapore"]:
        if place in text:
            destination = place.title()

    # Days
    match = re.search(r"(\d+)\s*(day|days)", text)
    if match:
        days = int(match.group(1))

    # Travel style
    if "solo" in text:
        travel_style = "solo"
    elif "family" in text:
        travel_style = "family"
    elif "couple" in text:
        travel_style = "couple"

    # Budget
    if "budget" in text or "cheap" in text:
        budget_type = "budget"
    elif "luxury" in text:
        budget_type = "luxury"
    elif "mid" in text:
        budget_type = "mid-range"

    return {
        "destination": destination,
        "days": days,
        "travel_style": travel_style,
        "budget_type": budget_type
    }
