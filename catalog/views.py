from django.views.generic import ListView
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
        qs = Product.objects.all().order_by("-id")
        form = self.get_form()
        if form.is_valid():
            q = form.cleaned_data.get("q")
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
        ctx["q"] = form.cleaned_data.get("q") if form.is_valid() else ""
        return ctx
