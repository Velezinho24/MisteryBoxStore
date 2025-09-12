from django.db import models

class PaymentTransaction(models.Model):
    GATEWAYS = [("stripe", "Stripe"), ("paypal", "PayPal"), ("mercadopago", "MercadoPago")]
    STATUSES = [("created", "Created"), ("pending", "Pending"), ("succeeded", "Succeeded"), ("failed", "Failed")]

    order = models.ForeignKey("orders.Order", related_name="payments", on_delete=models.CASCADE)
    gateway = models.CharField(max_length=20, choices=GATEWAYS)
    status = models.CharField(max_length=20, choices=STATUSES, default="created")
    external_id = models.CharField(max_length=128, blank=True)
    amount_cop = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="COP")
    raw_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gateway.upper()} {self.status} - {self.external_id or 'N/A'}"