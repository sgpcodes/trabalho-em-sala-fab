# ============================================================
# ===============  IMPORTAÇÕES E CONFIGURAÇÕES  ===============
# ============================================================

from __future__ import annotations
import os
import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pika

# ============================================================
# ===============  VARIÁVEIS DE AMBIENTE (.env)  ==============
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / ".env")

# URL de conexão com RabbitMQ (exemplo local)
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbit:5672/")

# ============================================================
# ==================  CONFIGURAÇÃO DO FASTAPI  ================
# ============================================================

app = FastAPI(title="FastAPI + RabbitMQ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# =================  CONEXÃO COM RABBITMQ  ====================
# ============================================================

def send_to_queue(message: dict):
    """
    Envia uma mensagem JSON para a fila 'mensagens' no RabbitMQ.
    """
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Cria fila persistente
    channel.queue_declare(queue='mensagens', durable=True)

    # Publica mensagem
    channel.basic_publish(
        exchange='',
        routing_key='mensagens',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # persistente
    )

    print(f"[x] Mensagem enviada: {message}")
    connection.close()


# ============================================================
# ===============  ENDPOINT /enviar (REST API)  ===============
# ============================================================

@app.post("/enviar")
async def enviar_mensagem(payload: dict):
    """
    Recebe um JSON {"nome": "Maria", "texto": "Oi!"}
    e envia para a fila RabbitMQ.
    """
    send_to_queue(payload)
    return {"status": "mensagem enviada", "conteudo": payload}


@app.get("/")
def health_check():
    return {"message": "API rodando!"}


# ============================================================
# ======================  FIM DO ARQUIVO  =====================
# ============================================================
