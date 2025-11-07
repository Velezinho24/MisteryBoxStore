# mistery_boxes/urls.py
from django.urls import path
from . import views

app_name = "mystery_boxes"

urlpatterns = [
    path("create/", views.mysterybox_create, name="create"),
    path("", views.mysterybox_list, name="list"),
    path("buy/<int:box_id>/", views.buy_mystery_box, name="buy"),
    path("reveal/", views.mystery_box_reveal, name="reveal"),
    path("<slug:slug>/", views.mysterybox_detail, name="detail"),
]
