import re

def extract_days(text):
    match = re.search(r"(\d+)\s*(day|days)?", text.lower())
    return int(match.group(1)) if match else None

def extract_travel_style(text):
    for s in ["solo", "family", "couple"]:
        if s in text.lower():
            return s
    return None

def extract_budget(text):
    for b in ["budget", "mid-range", "luxury"]:
        if b in text.lower():
            return b
    return None

def extract_destination(text):
    match = re.search(r"(to|visit|in)\s+([a-zA-Z\s]+)", text.lower())
    if match:
        return match.group(2).strip().title()
    return None
