import pika
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class RabbitMQProducer:
    """
    Productor de mensajes para RabbitMQ
    Publica eventos cuando se crea un nuevo cliente
    """
    
    def __init__(self):
        self.rabbitmq_url = settings.RABBITMQ_URL
        self.exchange_name = settings.CUSTOMERS_EXCHANGE
        self.connection = None
        self.channel = None
        logger.info(f"RabbitMQProducer inicializado - URL: {self.rabbitmq_url}, Exchange: {self.exchange_name}")

    def connect(self):
        """
        Establece conexión con RabbitMQ
        """
        try:
            logger.info("Intentando conectar a RabbitMQ...")
            parameters = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declarar exchange tipo fanout para broadcast
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='fanout',
                durable=True
            )
            
            logger.info(f"Conectado a RabbitMQ - Exchange: {self.exchange_name}")
            return True
        except Exception as e:
            logger.error(f"Error conectando a RabbitMQ: {str(e)}", exc_info=True)
            return False

    def publish_customer_created(self, customer_data):
        """
        Publica evento de cliente creado
        """
        logger.info(f"Iniciando publicación de evento para cliente ID: {customer_data.get('id')}")
        
        try:
            if not self.channel:
                logger.info("Canal no existe, intentando conectar...")
                if not self.connect():
                    logger.error("No se pudo conectar a RabbitMQ")
                    return False

            message = {
                'event': 'customer.created',
                'data': customer_data
            }
            
            logger.info(f"Publicando mensaje: {json.dumps(message)}")

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key='',  # No se usa en fanout
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Mensaje persistente
                    content_type='application/json'
                )
            )

            logger.info(f"✅ Evento publicado exitosamente: customer.created - ID: {customer_data.get('id')}, Email: {customer_data.get('email')}")
            return True

        except Exception as e:
            logger.error(f"❌ Error publicando mensaje: {str(e)}", exc_info=True)
            self.close()
            return False

    def close(self):
        """
        Cierra la conexión con RabbitMQ
        """
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
                logger.info("Conexión a RabbitMQ cerrada")
        except Exception as e:
            logger.error(f"Error cerrando conexión: {str(e)}")


# Instancia global del productor
producer = RabbitMQProducer()
