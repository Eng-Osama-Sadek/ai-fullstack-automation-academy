import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ضبط المسار الرئيسي للمشروع
BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "AI Software Learner" and BASE_DIR.parent != BASE_DIR:
    BASE_DIR = BASE_DIR.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ai_dev_academy.services.ai_engine import AITutorEngine

app = FastAPI(title="AI Full-Stack & Automation Academy API", version="1.0.0")

class PromptRequest(BaseModel):
    prompt: str
    track: str
    api_key: str | None = None

@app.get("/")
async def root():
    return {"status": "online", "message": "API is running smoothly!"}

@app.post("/api/v1/ask-tutor")
async def ask_tutor_endpoint(request: PromptRequest):
    try:
        tutor = AITutorEngine(api_key=request.api_key)
        response = tutor.ask_tutor(prompt=request.prompt, context=request.track)
        return {"status": "success", "track": request.track, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))