import pika
import json
import logging
import sys
import os
import django
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_ms.settings')
django.setup()

from django.conf import settings
from api.models import EmailLog
from api.email_service import EmailService

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailConsumer:
    """
    Consumidor de eventos de RabbitMQ para el servicio de emails
    Escucha eventos de customer.created y envía correos de bienvenida
    """
    
    def __init__(self):
        self.rabbitmq_url = settings.RABBITMQ_URL
        self.exchange_name = settings.CUSTOMERS_EXCHANGE
        self.queue_name = settings.EMAIL_QUEUE
        self.connection = None
        self.channel = None
        self.email_service = EmailService()

    def connect(self):
        """
        Establece conexión con RabbitMQ con reintentos
        """
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Intentando conectar a RabbitMQ (intento {attempt + 1}/{max_retries})...")
                parameters = pika.URLParameters(self.rabbitmq_url)
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                
                # Declarar exchange
                self.channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type='fanout',
                    durable=True
                )
                
                # Declarar cola
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                
                # Vincular cola al exchange
                self.channel.queue_bind(
                    exchange=self.exchange_name,
                    queue=self.queue_name
                )
                
                logger.info(f"Conectado a RabbitMQ - Queue: {self.queue_name}")
                return True
                
            except Exception as e:
                logger.error(f"Error conectando a RabbitMQ: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    logger.error("No se pudo conectar a RabbitMQ después de varios intentos")
                    return False

    def callback(self, ch, method, properties, body):
        """
        Callback que se ejecuta cuando llega un mensaje
        """
        try:
            message = json.loads(body)
            event = message.get('event')
            data = message.get('data', {})
            
            logger.info(f"Mensaje recibido: {event}")
            
            if event == 'customer.created':
                self.handle_customer_created(data)
            
            # Confirmar mensaje procesado
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")
            # Rechazar mensaje y no reencolar
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def handle_customer_created(self, customer_data):
        """
        Maneja el evento de cliente creado
        Envía correo de bienvenida al nuevo cliente
        """
        try:
            customer_id = customer_data.get('id')
            customer_email = customer_data.get('email')
            customer_name = f"{customer_data.get('first_name', '')} {customer_data.get('last_name', '')}"
            
            # Enviar email de bienvenida
            success, subject, body = self.email_service.send_welcome_email(
                customer_name,
                customer_email
            )
            
            # Registrar en base de datos
            email_log = EmailLog.objects.create(
                customer_id=customer_id,
                customer_email=customer_email,
                customer_name=customer_name,
                email_type='welcome',
                subject=subject if subject else 'Email de bienvenida',
                body=body if body else '',
                status='sent' if success else 'failed',
                error_message=None if success else 'Error al enviar email',
                sent_at=datetime.now() if success else None
            )
            
            if success:
                logger.info(
                    f"Email de bienvenida enviado a: {customer_email} "
                    f"(Cliente ID: {customer_id}) - Log ID: {email_log.id}"
                )
            else:
                logger.error(f"Falló el envío de email a: {customer_email}")
            
        except Exception as e:
            logger.error(f"Error enviando email de bienvenida: {str(e)}")
            raise

    def start_consuming(self):
        """
        Inicia el consumo de mensajes
        """
        try:
            if not self.connect():
                sys.exit(1)
            
            # Configurar QoS
            self.channel.basic_qos(prefetch_count=1)
            
            # Iniciar consumo
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self.callback
            )
            
            logger.info(f"Esperando mensajes en cola: {self.queue_name}...")
            logger.info("Presiona CTRL+C para salir")
            
            self.channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Consumidor detenido por el usuario")
            self.stop()
        except Exception as e:
            logger.error(f"Error en el consumidor: {str(e)}")
            self.stop()
            sys.exit(1)

    def stop(self):
        """
        Detiene el consumidor y cierra conexiones
        """
        try:
            if self.channel:
                self.channel.stop_consuming()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("Consumidor detenido correctamente")
        except Exception as e:
            logger.error(f"Error deteniendo consumidor: {str(e)}")


if __name__ == '__main__':
    consumer = EmailConsumer()
    consumer.start_consuming()
