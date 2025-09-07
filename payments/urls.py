from django.urls import path
from django.views.generic import TemplateView

app_name = "payments"
urlpatterns = [
    path("checkout/", TemplateView.as_view(template_name="payments/checkout.html"), name="checkout"),
    path("success/", TemplateView.as_view(template_name="payments/success.html"), name="success"),
]
