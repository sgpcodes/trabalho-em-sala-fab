# ============================================================
# ===============  CONSUMIDOR DE MENSAGENS  ==================
# ============================================================

import pika
import json
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"[✔] Mensagem recebida: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='mensagens', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='mensagens', on_message_callback=callback)

    print("[*] Aguardando mensagens. Pressione CTRL+C para sair.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
