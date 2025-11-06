from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from mistery_boxes.models import MysteryBox
from catalog.models import Product
import random


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Mystery boxes reales (máximo 4 para el home)
        ctx["boxes"] = MysteryBox.objects.filter(is_active=True).prefetch_related('products')[:4]

        # Productos destacados reales (6 productos aleatorios)
        all_products = list(Product.objects.filter(is_active=True).prefetch_related('mystery_boxes'))
        ctx["featured_products"] = random.sample(all_products, min(6, len(all_products)))

        # Estadísticas reales
        total_boxes = MysteryBox.objects.filter(is_active=True).count()
        total_products = Product.objects.filter(is_active=True).count()
        products_in_boxes = Product.objects.filter(mystery_boxes__isnull=False, is_active=True).distinct().count()
        
        ctx["stats"] = {
            "boxes_count": total_boxes,
            "products_count": total_products,
            "products_in_boxes": products_in_boxes,
        }

        return ctx
