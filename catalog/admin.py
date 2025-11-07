from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "product_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_per_page = 20
    
    def product_count(self, obj):
        count = obj.products.count()
        return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', count)
    product_count.short_description = "Products"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price_display", "is_active", "image_preview")
    list_filter = ("is_active", "category")
    search_fields = ("name", "tags", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active",)
    list_per_page = 20
    readonly_fields = ("image_preview_large",)
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "category", "is_active")
        }),
        ("Pricing", {
            "fields": ("price_cop",)
        }),
        ("Media", {
            "fields": ("image", "image_preview_large")
        }),
        ("Additional Information", {
            "fields": ("tags",),
            "classes": ("collapse",)
        }),
    )
    
    def price_display(self, obj):
        return format_html('<span style="color: #dc3545; font-weight: bold;">$ {}</span>', f'{obj.price_cop:,}')
    price_display.short_description = "Price (COP)"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" style="border-radius: 10px;" />', obj.image.url)
        return "No image uploaded"
    image_preview_large.short_description = "Current Image"