from dotenv import load_dotenv
import os
from google import genai
from main import szukany_szachista

load_dotenv()
klucz = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=klucz)

historia = []
dziala = True

while dziala:  
    # zapytanie
    user_input=str(input("Enter username on chess.com: "))
    #historia.append({"role": "user", "parts": [{"text": user_input}]})
    #print(historia)
    if user_input.lower() == "koniec":
        dziala = False
        break
    chesscom_result = szukany_szachista(wyszukany_zawodnik=user_input)
    historia.append({"role": "user", "parts": [{"text": f"Player data: {chesscom_result}"}]})
    historia.append({"role": "model", "parts": [{"text": "I understand, I can answer questions about this player"}]})
    while True:
        user_question = str(input(f"What do you want to know about: {user_input}? "))
        historia.append({"role": "user", "parts": [{"text": user_question}]})
        if user_question.lower() == "change player":
            historia.append({"role": "model", "parts": [{"text": "change player"}]})
            historia = []
            break
        elif user_question.lower() == "exit":
            historia.append({"role": "model", "parts": [{"text": "exit"}]})
            historia = []
            dziala = False
            break
        else:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=historia
            )
            historia.append({"role": "model", "parts": [{"text": response.text}]})

            print(response.text)