from django.contrib import admin
from .models import MysteryBox


@admin.register(MysteryBox)
class MysteryBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_cop", "is_active", "get_products_count")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("products",)

    def get_products_count(self, obj):
        return obj.products.count()
    get_products_count.short_description = "Productos"
