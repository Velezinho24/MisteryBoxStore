from django.contrib import admin
from django.utils.html import format_html
from .models import MysteryBox


@admin.register(MysteryBox)
class MysteryBoxAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price_display", "is_active", "product_count", "image_preview")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description", "slug")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("products",)
    list_editable = ("is_active",)
    list_per_page = 20
    readonly_fields = ("image_preview_large", "statistics")
    
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "category", "is_active")
        }),
        ("Pricing", {
            "fields": ("price_cop",)
        }),
        ("Description", {
            "fields": ("description",)
        }),
        ("Media", {
            "fields": ("image", "image_preview_large")
        }),
        ("Products", {
            "fields": ("products", "statistics"),
            "description": "Select the products that can be won in this mystery box"
        }),
    )

    def price_display(self, obj):
        return format_html('<span style="color: #dc3545; font-weight: bold;">$ {}</span>', f'{obj.price_cop:,}')
    price_display.short_description = "Price (COP)"
    
    def product_count(self, obj):
        count = obj.products.count()
        color = "#28a745" if count > 0 else "#dc3545"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, count)
    product_count.short_description = "Products"
    
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
    
    def statistics(self, obj):
        if not obj.pk:
            return "Save the mystery box first to see statistics"
        
        products = obj.products.all()
        if not products:
            return format_html('<p style="color: #dc3545;">No products added yet</p>')
        
        total = products.count()
        min_price = min(p.price_cop for p in products)
        max_price = max(p.price_cop for p in products)
        avg_price = sum(p.price_cop for p in products) / total
        
        html = f"""
        <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #dc3545;">
            <h4 style="margin-top: 0;">📊 Mystery Box Statistics</h4>
            <ul style="list-style: none; padding: 0;">
                <li>🎁 <strong>Total Products:</strong> {total}</li>
                <li>💰 <strong>Box Price:</strong> $ {obj.price_cop:,} COP</li>
                <li>📉 <strong>Min Product Value:</strong> $ {min_price:,} COP</li>
                <li>📊 <strong>Avg Product Value:</strong> $ {avg_price:,.0f} COP</li>
                <li>📈 <strong>Max Product Value:</strong> $ {max_price:,} COP</li>
                <li>🎯 <strong>Potential Gain:</strong> $ {max_price - obj.price_cop:,} COP ({((max_price / obj.price_cop - 1) * 100):.1f}%)</li>
            </ul>
        </div>
        """
        return format_html(html)
    statistics.short_description = "Statistics"
