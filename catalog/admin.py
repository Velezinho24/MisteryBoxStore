from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_cop", "tags")
    list_filter = ("tags",)
    search_fields = ("name", "tags")