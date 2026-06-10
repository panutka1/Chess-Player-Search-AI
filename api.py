from fastapi import FastAPI
from main import szukany_szachista
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from rag import search_and_response

app = FastAPI()

load_dotenv()
klucz = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=klucz)

class ChatRequest(BaseModel):
    nazwa: str
    pytanie: str

class QuestionModel(BaseModel):
    question: str

@app.get("/")
def index():
    return {"message": "It works!"}

@app.get("/player/{nazwa}")
def get_zawodnik(nazwa):
    result = szukany_szachista(wyszukany_zawodnik=nazwa)
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    historia = []
    chesscom_result = szukany_szachista(wyszukany_zawodnik=request.nazwa)
    historia.append({"role": "user", "parts": [{"text": f"Player data: {chesscom_result}"}]})
    historia.append({"role": "model", "parts": [{"text": "I understand, I can answer questions about this player"}]})
    historia.append({"role": "user", "parts": [{"text": request.pytanie}]})
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction='''You are a chess expert assistant.
                                    Answer in English.
                                    Use the provided context whenever it is relevant.
                                    You may use your general chess knowledge to supplement the answer.

                                    If the context and your knowledge are insufficient to answer the question, say:
                                    "I don't know."
                                    Prefer information from the provided context when there is a conflict.''',
            temperature=0.3
        ),
        contents=historia
    )
    historia.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text

@app.post("/rag")
def rag(request: QuestionModel):
    result = search_and_response(request.question)
    return result
