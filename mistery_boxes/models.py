from django.db import models
from catalog.models import Product, Category


class MysteryBox(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price_cop = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="mystery_boxes/", blank=True, null=True, default="mystery_boxes/default.png")
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, 
        related_name="mystery_boxes",
        null=True,
        blank=True,
        help_text="Categoría principal de esta caja misteriosa"
    )
    products = models.ManyToManyField(Product, related_name="mystery_boxes")

    def __str__(self):
        return self.name
