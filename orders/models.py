from django.db import models
from customer.models import Customer


class Orders(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order for {self.item} by {self.customer.name}"