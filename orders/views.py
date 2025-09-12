from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from .services import get_or_create_cart, add_item, set_quantity, remove_item
from .models import CartItem

# Importa tus modelos reales
from catalog.models import Product
from mistery_boxes.models import MysteryBox

def cart_detail(request):
    cart = get_or_create_cart(request)
    context = {
        "cart": cart,
        "items": cart.items.select_related("content_type"),
    }
    return render(request, "orders/cart.html", context)

@require_POST
def add_to_cart(request):
    cart = get_or_create_cart(request)
    item_type = request.POST.get("type")            # "product" | "box"
    object_id = request.POST.get("id")              # debería ser un int como str
    qty_raw = request.POST.get("qty", "1")

    if not item_type or item_type not in {"product", "box"}:
        messages.error(request, "Tipo de ítem inválido.")
        return redirect("orders:cart_detail")

    if not object_id or not object_id.isdigit():
        messages.error(request, "ID de ítem inválido.")
        return redirect("orders:cart_detail")

    try:
        qty = int(qty_raw)
    except ValueError:
        qty = 1
    if qty <= 0:
        messages.error(request, "La cantidad debe ser mayor a 0.")
        return redirect("orders:cart_detail")

    if item_type == "product":
        obj = get_object_or_404(Product, pk=int(object_id), is_active=True)
    else:  # "box"
        obj = get_object_or_404(MysteryBox, pk=int(object_id), is_active=True)

    add_item(cart, obj, qty)
    messages.success(request, "Agregado al carrito.")
    return redirect("orders:cart_detail")

@require_POST
def update_quantity(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get("qty", 1))
    set_quantity(item, qty)
    messages.success(request, "Cantidad actualizada.")
    return redirect("orders:cart_detail")

@require_POST
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    remove_item(item)
    messages.info(request, "Ítem eliminado.")
    return redirect("orders:cart_detail")