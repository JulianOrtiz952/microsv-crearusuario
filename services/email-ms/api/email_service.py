import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Servicio para enviar correos electrónicos
    En desarrollo usa console backend, en producción se puede configurar SMTP
    """
    
    @staticmethod
    def send_welcome_email(customer_name, customer_email):
        """
        Envía correo de bienvenida a un nuevo cliente
        """
        try:
            subject = f"¡Bienvenido/a {customer_name}!"
            
            body = f"""
            Hola {customer_name},

            ¡Bienvenido/a a nuestra plataforma!

            Estamos muy contentos de tenerte con nosotros. Tu cuenta ha sido creada exitosamente.

            Como nuevo cliente, has recibido:
            - Puntos de lealtad inicializados (comienza a acumular puntos con tus compras)
            - Un paquete de bienvenida que será enviado a tu dirección

            Si tienes alguna pregunta, no dudes en contactarnos.

            ¡Gracias por unirte a nosotros!

            Saludos,
            El equipo de Tu Empresa
            """
            
            # En desarrollo, esto imprime en consola
            # En producción, configurar SMTP real
            logger.info(f"Enviando email de bienvenida a: {customer_email}")
            logger.info(f"Asunto: {subject}")
            logger.info(f"Cuerpo:\n{body}")
            
            # Simular envío exitoso
            return True, subject, body
            
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False, None, None
