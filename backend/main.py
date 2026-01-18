from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import build_graph

app = FastAPI(title="TripMind AI")

# ================= CORS CONFIG =================
# Replace these with your actual frontend URLs
FRONTEND_URLS = [
    "http://localhost:5173",                       # local dev
    "https://trip-mind-ai-six.vercel.app/"       # deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_URLS,  # frontend only
    allow_credentials=True,
    allow_methods=["*"],           # GET, POST, OPTIONS
    allow_headers=["*"],           # Content-Type, Authorization, etc.
)

# ================= CHATBOT =================
chatbot = build_graph()

class ChatRequest(BaseModel):
    message: str

# ================= HEALTH CHECK =================
@app.get("/")
def root():
    return {"status": "ok"}

# ================= OPTIONS PREFLIGHT =================
# This ensures any OPTIONS request won't fail on Render
@app.options("/{path:path}")
def preflight_handler(path: str):
    return {}

# ================= CHAT ENDPOINT =================
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        if not req.message:
            return {
                "reply": "⚠️ Message cannot be empty.",
                "complete": True
            }

        result = chatbot({"message": req.message})

        # Defensive checks (critical for production)
        if result is None:
            raise ValueError("Chatbot returned None")

        if not isinstance(result, dict):
            raise ValueError(f"Invalid chatbot response type: {type(result)}")

        reply = result.get("reply")
        if not reply:
            reply = "⚠️ I couldn't generate a response."

        return {
            "reply": reply,
            "complete": result.get("complete", False)
        }

    except Exception as e:
        # This WILL appear in Render logs
        print("🔥 CHAT ERROR:", repr(e))

        return {
            "reply": "❌ Internal server error. Please try again.",
            "complete": True
        }

# ================= RUN FOR LOCAL DEV (optional) =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
