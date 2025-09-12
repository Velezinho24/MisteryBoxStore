from django.shortcuts import render
from .models import MysteryBox

def box_list(request):
    boxes = MysteryBox.objects.filter(is_active=True)
    return render(request, "mistery_boxes/box_list.html", {"boxes": boxes})