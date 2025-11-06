from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True, default="products/default.png")
    tags = models.CharField(max_length=255, help_text=_("Comma-separated tags"), blank=True)
    price_cop = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products",
        null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name