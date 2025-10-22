from django.db import models


class Delivery(models.Model):
    """
    Modelo para almacenar envíos de paquetes de bienvenida
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'En proceso'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregado'),
        ('cancelled', 'Cancelado'),
    ]
    
    customer_id = models.IntegerField(verbose_name="ID del Cliente")
    customer_email = models.EmailField(verbose_name="Email del Cliente")
    customer_name = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    customer_address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    
    package_type = models.CharField(
        max_length=100,
        default='welcome_package',
        verbose_name="Tipo de paquete"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Número de seguimiento"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de envío")
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de entrega")

    class Meta:
        db_table = 'deliveries'
        verbose_name = 'Envío'
        verbose_name_plural = 'Envíos'
        ordering = ['-created_at']

    def __str__(self):
        return f"Envío #{self.id} - {self.customer_name} ({self.status})"

    def update_status(self, new_status):
        """
        Actualiza el estado del envío
        """
        self.status = new_status
        self.save()
