from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class Request(BaseModel):
    topic: str

@app.get("/")
def get_root():
    return {"message" : "Xin chào Milynx"}

@app.post("/generate")
def generate_mcq(req: Request):
    try:
        prompt = f"""
        Generate 1 multiple choice question about: {req.topic}

        Return JSON format:
        {{
            "question": "...",
            "options": ["A", "B", "C", "D"],
            "answer": "A"
        }}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text
        try:
            parsed = json.loads(response_text)
            return parsed
        except:
            return {"raw": response_text}
            
    except Exception as e:
        return {"error": str(e)}