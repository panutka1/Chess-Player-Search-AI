from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import chromadb
from pdf_reader import read_pdf

load_dotenv()
klucz = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(api_key=klucz)

client_chroma = chromadb.PersistentClient("./chroma")
collection = client_chroma.get_or_create_collection(name="chess_players")

def search(user_input):
    question_result = client_ai.models.embed_content(
    model="gemini-embedding-001",
    contents=user_input,
    config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    wyniki = collection.query(
    query_embeddings=[question_result.embeddings[0].values],
    n_results=3
    )
    return wyniki["documents"][0]

def init_db():
    PATH = "players_info.pdf"

    #-------Reading txt files-------
    #with open(PATH, "r", encoding="utf-8") as f:
    #    file = f.read()

    file = read_pdf(PATH)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
    texts = text_splitter.split_text(file)

    #print(texts)
    #print(len(texts))

    #print(collection.count())
    if collection.count() == 0:
        result = client_ai.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
        )
        print("Liczba chunków:", len(texts))
        print("Liczba embeddingów:", len(result.embeddings))
        print(len(result.embeddings[0].values))
        collection.add(
            ids = [f"id{i}" for i in range(1, len(texts) + 1)],
            embeddings=[e.values for e in result.embeddings],
            documents=texts,
        )
        data = collection.get()
        #print(data.keys())
        #print(len(data["ids"]))
        #print(len(data["documents"]))



def conversation(question, context):
    historia = []
    historia.append({"role": "user", "parts": [{"text": f"Odpowiedz na pytanie {question} na podstawie danych {context}"}]})
    
    response = client_ai.models.generate_content(
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

    return(response.text)

def search_and_response(question):
    results = search(question)
    context = "\n".join(results)
    return conversation(question, context)
