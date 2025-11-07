from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return sum((item.line_total for item in self.items.all()), 0)

    @property
    def total(self):
        # Si luego agregas envío o cupones, ajusta aquí.
        return self.subtotal

    def __str__(self):
        owner = self.user or self.session_key or "anon"
        return f"Cart<{owner}>"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)

    # Apunta a Product o MysteryBox
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    quantity = models.PositiveIntegerField(default=1)
    unit_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price_snapshot

    def __str__(self):
        return f"{self.content_object} x {self.quantity}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("canceled", "Canceled"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    total_cop = models.PositiveIntegerField() 
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_invoice = models.FileField(upload_to="invoices/", null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price_cop = models.PositiveIntegerField()
    line_total_cop = models.PositiveIntegerField()
    
    # Para mystery boxes: el producto ganado
    won_product = models.ForeignKey(
        'catalog.Product', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='won_in_orders',
        help_text="Si este item es una mystery box, este campo indica qué producto se ganó"
    )
    
    # Indica si este item es una mystery box
    is_mystery_box = models.BooleanField(default=False)
    mystery_box_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} x {self.quantity}"