from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MysteryBox
from .forms import MysteryBoxForm


@login_required
def mysterybox_list(request):
    boxes = MysteryBox.objects.filter(is_active=True)
    return render(request, "mysteryboxes/box_list.html", {"boxes": boxes})


@login_required
def mysterybox_create(request):
    if request.method == "POST":
        form = MysteryBoxForm(request.POST, request.FILES)
        if form.is_valid():
            box = form.save(commit=False)
            selected_products = form.cleaned_data["products"]

            total_price = sum(p.price_cop for p in selected_products)
            box.price_cop = int(total_price * 0.8)
            box.save()

            # guardar relación M2M
            box.products.set(selected_products)

            messages.success(
                request,
                f"Caja '{box.name}' creada con {selected_products.count()} productos."
                )
            return redirect("mystery_boxes:list")
    else:
        form = MysteryBoxForm()

    return render(request, "mysteryboxes/box_form.html", {"form": form})


@login_required
def mysterybox_detail(request, slug):
    box = get_object_or_404(MysteryBox, slug=slug, is_active=True)
    products = box.products.filter(is_active=True)

    return render(request, "mysteryboxes/box_detail.html", {
        "box": box,
        "products": products,
    })
