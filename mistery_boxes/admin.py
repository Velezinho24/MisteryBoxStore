from django.contrib import admin
from .models import MysteryBox

@admin.register(MysteryBox)
class MysteryBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_cop", "is_active")
    list_filter = ("is_active", "category")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")