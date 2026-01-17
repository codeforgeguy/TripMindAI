from typing import Optional, Literal
from pydantic import BaseModel


class TripState(BaseModel):
    session_id: str

    # Classification
    category: Optional[Literal[
        "itinerary_planning",
        "budget_travel",
        "luxury_travel"
    ]] = None

    # Trip details
    user_name: Optional[str] = None
    destination: Optional[str] = None
    days: Optional[int] = None
    travel_style: Optional[str] = None
    budget_range: Optional[str] = None

    # Completion
    complete: bool = False
