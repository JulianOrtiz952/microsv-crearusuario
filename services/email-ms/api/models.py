from django.db import models


class EmailLog(models.Model):
    """
    Modelo para registrar envíos de correos electrónicos
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]
    
    EMAIL_TYPE_CHOICES = [
        ('welcome', 'Bienvenida'),
        ('notification', 'Notificación'),
        ('promotional', 'Promocional'),
    ]
    
    customer_id = models.IntegerField(verbose_name="ID del Cliente")
    customer_email = models.EmailField(verbose_name="Email del Cliente")
    customer_name = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    
    email_type = models.CharField(
        max_length=50,
        choices=EMAIL_TYPE_CHOICES,
        default='welcome',
        verbose_name="Tipo de email"
    )
    subject = models.CharField(max_length=200, verbose_name="Asunto")
    body = models.TextField(verbose_name="Cuerpo del mensaje")
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mensaje de error"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de envío")

    class Meta:
        db_table = 'email_logs'
        verbose_name = 'Log de Email'
        verbose_name_plural = 'Logs de Emails'
        ordering = ['-created_at']

    def __str__(self):
        return f"Email #{self.id} - {self.customer_email} ({self.status})"
