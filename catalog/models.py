from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    tags = models.CharField(max_length=255, help_text=_("Comma-separated tags"))
    price_cop = models.PositiveIntegerField()

    def __str__(self):
        return self.name