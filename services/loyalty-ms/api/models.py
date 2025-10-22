from django.db import models


class LoyaltyPoints(models.Model):
    """
    Modelo para almacenar puntos de lealtad de clientes
    """
    customer_id = models.IntegerField(unique=True, verbose_name="ID del Cliente")
    customer_email = models.EmailField(verbose_name="Email del Cliente")
    customer_name = models.CharField(max_length=200, verbose_name="Nombre del Cliente")
    points = models.IntegerField(default=0, verbose_name="Puntos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        db_table = 'loyalty_points'
        verbose_name = 'Puntos de Lealtad'
        verbose_name_plural = 'Puntos de Lealtad'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.points} puntos"

    def add_points(self, points):
        """
        Añade puntos al cliente
        """
        self.points += points
        self.save()

    def subtract_points(self, points):
        """
        Resta puntos al cliente
        """
        if self.points >= points:
            self.points -= points
            self.save()
            return True
        return False
