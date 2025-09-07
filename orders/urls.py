from django.urls import path
from django.views.generic import TemplateView

app_name = "orders"
urlpatterns = [
    path("", TemplateView.as_view(template_name="orders/cart.html"), name="list"),
    path("create/", TemplateView.as_view(template_name="orders/create.html"), name="create"),
]
