from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_trip(data: dict):
    # save only when conversation is complete
    if not data.get("complete"):
        return

    payload = {
        "destination": data.get("destination"),
        "days": data.get("days"),
        "travel_style": data.get("travel_style"),
        "budget_range": data.get("budget_range"),
        "category": data.get("category"),
    }

    supabase.table("travel_plans").insert(payload).execute()
