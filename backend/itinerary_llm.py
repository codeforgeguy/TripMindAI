def generate_itinerary(state: dict) -> str:
    destination = state["destination"]
    days = int(state["days"])
    travel_style = state["travel_style"]
    budget = state["budget_type"]

    base_plan = [
        "Arrival and hotel check-in, light exploration",
        "Local sightseeing and cultural spots",
        "Adventure activities & local experiences",
        "Leisure day with shopping and food exploration",
        "Hidden gems and relaxation",
        "Optional excursions or free day",
        "Leisure & departure preparation"
    ]

    itinerary_days = []
    for i in range(days):
        activity = base_plan[i % len(base_plan)]
        itinerary_days.append(f"🗓️Day {i+1}: {activity} in {destination}")

    itinerary_text = "\n".join(itinerary_days)

    return f"""
✈️ Your trip is ready!

📍 Destination: {destination}
⌛ Duration: {days} days
👤 Travel style: {travel_style.title()}
💰 Budget: {budget.title()}

👇 Suggested Itinerary
{itinerary_text}
""".strip()
