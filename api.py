from fastapi import FastAPI
from main import chess_player_search
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
from google.genai import types
from rag import search_and_response

app = FastAPI()

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

class ChatRequest(BaseModel):
    name: str
    question: str

class QuestionModel(BaseModel):
    question: str

@app.get("/")
def index():
    return {"message": "It works!"}

@app.get("/player/{name}")
def get_player(name):
    result = chess_player_search(player=name)
    return result

@app.post("/chat")
def chat(request: ChatRequest):
    client = genai.Client(api_key=key)
    history = []
    chesscom_result = chess_player_search(player=request.name)
    history.append({"role": "user", "parts": [{"text": f"Player data: {chesscom_result}"}]})
    history.append({"role": "model", "parts": [{"text": "I understand, I can answer questions about this player"}]})
    history.append({"role": "user", "parts": [{"text": request.question}]})
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
        contents=history
    )
    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text

@app.post("/rag")
def rag(request: QuestionModel):
    result = search_and_response(request.question)
    return result
