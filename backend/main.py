from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://trip-mind-ai-six.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbot = build_graph()

class ChatRequest(BaseModel):
    message: str

# Health check route
@app.get("/")
def root():
    return {"status": "ok"}

# Existing chat route
@app.post("/chat")
def chat(req: ChatRequest):
    result = chatbot({"message": req.message})
    return {
        "reply": result["reply"],
        "complete": result.get("complete", False)
    }
