from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import build_graph

app = FastAPI()

# 🔥 SAFE CORS (production debug mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = build_graph()

class ChatRequest(BaseModel):
    message: str

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

@app.options("/{path:path}")
def preflight_handler(path: str):
    return {}

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
