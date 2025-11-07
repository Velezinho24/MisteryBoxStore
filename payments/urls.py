from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/", RedirectView.as_view(pattern_name="payments:checkout_start", permanent=False)),
    path("checkout/start/", views.checkout_start, name="checkout_start"),
    path("checkout/box/<int:order_id>/", views.checkout_start_box, name="checkout_start_box"),
    path("checkout/confirm/<int:order_id>/", views.checkout_confirm_dummy, name="checkout_confirm_dummy"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("webhooks/stripe/", views.stripe_webhook, name="stripe_webhook"),
]