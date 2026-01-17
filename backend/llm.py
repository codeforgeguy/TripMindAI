def generate_itinerary(state: dict) -> str:
    destination = state["destination"]
    days = state["days"]
    travel_style = state["travel_style"]
    budget = state["budget_type"]

    return f"""
✈️ **Your Trip is Ready!**

**Destination:** {destination}
**Duration:** {days} days
**Travel Style:** {travel_style.title()}
**Budget:** {budget.title()}

Here’s your personalized plan 👇

🗓 **Day 1 – Arrival**
• Arrive in {destination}
• Check into a luxury stay
• Relax and unwind after travel

🗓 **Day 2 – Local Exploration**
• Visit popular sightseeing spots
• Explore markets and cafés
• Enjoy authentic local cuisine

🗓 **Day 3 – Experiences & Culture**
• Cultural attractions and landmarks
• Guided tours or experiences
• Evening leisure time

🗓 **Day 4 – Relaxation**
• Free morning
• Spa, beach, or café hopping
• Sunset views and dinner

🗓 **Remaining Days**
• Mix of sightseeing and relaxation
• Explore hidden gems
• Shop and enjoy local life

💰 **Estimated Budget:** Based on a {budget} trip style

Would you like recommendations for **hotels**, **food**, or **activities** next? 😊
""".strip()
