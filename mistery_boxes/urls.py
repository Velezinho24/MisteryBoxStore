from django.urls import path
from django.views.generic import TemplateView

app_name = "mistery_boxes"
urlpatterns = [
    path("", TemplateView.as_view(template_name="mistery_boxes/list.html"), name="list"),
    path("<slug:slug>/", TemplateView.as_view(template_name="mistery_boxes/detail.html"), name="detail"),
]
