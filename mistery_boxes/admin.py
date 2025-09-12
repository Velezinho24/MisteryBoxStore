from django.contrib import admin
from .models import MysteryBox


@admin.register(MysteryBox)
class MysteryBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "price_cop", "get_products")
    list_filter = ("products",)

    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = "Productos"
