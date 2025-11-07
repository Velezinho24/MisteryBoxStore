from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from mistery_boxes.models import MysteryBox
from catalog.models import Product
import random
import requests
from django.http import JsonResponse

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

def surprise_quote(request):
    """
    Retorna una frase inspiradora o misteriosa desde una API pública externa.
    Ideal para mostrar en la cabecera de la página.
    """
    try:
        res = requests.get("https://zenquotes.io/api/random", timeout=5)
        if res.status_code == 200:
            data = res.json()[0]
            return JsonResponse({
                "quote": data.get("q", "La vida está llena de sorpresas."),
                "author": data.get("a", "Anónimo")
            })
    except Exception:
        pass
    return JsonResponse({
        "quote": "La vida está llena de sorpresas.",
        "author": "MysteryVault"
    })