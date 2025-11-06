from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price_cop", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("name", "tags", "slug")
    prepopulated_fields = {"slug": ("name",)}