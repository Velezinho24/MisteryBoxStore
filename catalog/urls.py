from django.urls import path
from .views import ProductListView, product_detail

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", product_detail, name="detail"),
]
