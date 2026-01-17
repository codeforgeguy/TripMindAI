# Simple in-memory state management for user sessions
STATE_STORE = {}

def get_state(session_id: str) -> dict:
    return STATE_STORE.get(session_id, {})

def save_state(session_id: str, state: dict):
    STATE_STORE[session_id] = state
