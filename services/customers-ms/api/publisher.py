import json, os, pika, uuid

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
EXCHANGE = os.getenv("CUSTOMERS_EXCHANGE", "customers")

def _conn():
    params = pika.URLParameters(RABBITMQ_URL)
    return pika.BlockingConnection(params)

def publish_customer_created(customer: dict):
    """
    customer: {"id": "...", "name": "...", "email": "...", "created_at": "..."}
    """
    event = {
        "id": str(uuid.uuid4()),           # idempotencia del evento
        "event": "customer.created",
        "version": 1,
        "occurred_at": customer["created_at"],
        "data": customer,
    }
    body = json.dumps(event).encode()

    conn = _conn()
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="fanout", durable=True)
    ch.basic_publish(exchange=EXCHANGE, routing_key="", body=body,
                     properties=pika.BasicProperties(content_type="application/json",
                                                    delivery_mode=2))
    conn.close()
