from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import Response
from graph import build_graph

app = FastAPI()

# 🔥 ABSOLUTE CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow everything
    allow_credentials=False,      # REQUIRED with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = build_graph()

class ChatRequest(BaseModel):
    message: str

# ✅ Root (GET + HEAD)
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

# ✅ EXPLICIT OPTIONS HANDLER (this is the killer fix)
@app.options("/chat")
def options_chat():
    return Response(status_code=200)

# ✅ Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = chatbot({"message": req.message})

        if not isinstance(result, dict):
            raise ValueError("Invalid chatbot response")

        return {
            "reply": result.get("reply", "⚠️ No reply generated"),
            "complete": result.get("complete", False)
        }

    except Exception as e:
        print("🔥 CHAT ERROR:", repr(e))
        return {
            "reply": "❌ Internal server error. Please try again.",
            "complete": True
        }
# ✅ Reset endpoint
@app.post("/chat/reset")
def reset_chat():
    """Resets the chatbot memory"""
    global chatbot
    chatbot = build_graph()
    return {"status": "reset"}