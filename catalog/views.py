from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils.translation import gettext as _
from .models import Product
from .forms import CatalogFilterForm


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_form(self):
        return CatalogFilterForm(self.request.GET or None)

    def get_queryset(self):
        qs = Product.objects.all().select_related('category').prefetch_related('mystery_boxes').order_by("-id")
        form = self.get_form()
        if form.is_valid():
            q = form.cleaned_data.get("q")
            category = form.cleaned_data.get("category")
            tags = form.cleaned_data.get("tags") or []
            price_min = form.cleaned_data.get("price_min")
            price_max = form.cleaned_data.get("price_max")
            order = form.cleaned_data.get("order") or "relevance"

            if q:
                q = q.strip()
                qs = qs.filter(
                    Q(name__icontains=q) |
                    Q(tags__icontains=q)
                )

            # category filter
            if category:
                qs = qs.filter(category=category)

            # tags
            for t in tags:
                qs = qs.filter(tags__icontains=t)

            # price range
            if price_min is not None:
                qs = qs.filter(price_cop__gte=price_min)
            if price_max is not None:
                qs = qs.filter(price_cop__lte=price_max)

            # ordering
            if order == "price_asc":
                qs = qs.order_by("price_cop", "name")
            elif order == "price_desc":
                qs = qs.order_by("-price_cop", "name")
            elif order == "name_asc":
                qs = qs.order_by("name")
            elif order == "name_desc":
                qs = qs.order_by("-name")
            else:
                pass

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = self.get_form()
        ctx["form"] = form
        ctx["total"] = self.get_queryset().count()
        ctx["active_tags"] = form.cleaned_data.get("tags") if form.is_valid() else []
        ctx["active_category"] = form.cleaned_data.get("category") if form.is_valid() else None
        ctx["q"] = form.cleaned_data.get("q") if form.is_valid() else ""
        return ctx


def product_detail(request, slug):
    """
    Vista de detalle de un producto individual.
    Muestra toda la información del producto y productos relacionados.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Productos relacionados (misma categoría, excluyendo el actual)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).prefetch_related('mystery_boxes')[:6]
    
    # Mystery boxes donde aparece este producto
    mystery_boxes = product.mystery_boxes.filter(is_active=True)
    
    return render(request, "catalog/product_detail.html", {
        "product": product,
        "related_products": related_products,
        "mystery_boxes": mystery_boxes,
    })
