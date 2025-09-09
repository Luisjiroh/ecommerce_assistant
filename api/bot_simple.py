from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 👇 Definimos el modelo de datos para recibir mensajes
class Message(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Bienvenido al bot con FastAPI 🚀"}

@app.post("/chat")
def chat(msg: Message):
    # 👇 Aquí puedes personalizar la lógica del bot
    return {"response": f"Tú dijiste: {msg.text}"}
