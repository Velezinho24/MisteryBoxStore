from django.urls import path
from django.views.generic import TemplateView
from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", TemplateView.as_view(template_name="orders/cart.html"), name="list"),
    path("create/", TemplateView.as_view(template_name="orders/create.html"), name="create"),
    path("", views.cart_detail, name="cart_detail"),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("update/<int:item_id>/", views.update_quantity, name="update_quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
]