from django.urls import path
from django.views.generic import TemplateView

app_name = "catalog"
urlpatterns = [
    path("", TemplateView.as_view(template_name="catalog/index.html"), name="list"),
]
