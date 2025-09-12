from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import CartItem
from .services import get_or_create_cart, add_item, set_quantity, remove_item

from catalog.models import Product
try:
    from mistery_boxes.models import MysteryBox
except Exception:
    MysteryBox = None


def cart_detail(request):
    """Muestra el carrito actual (por sesión/usuario)."""
    cart = get_or_create_cart(request)
    items = cart.items.select_related("content_type")
    return render(request, "orders/cart.html", {"cart": cart, "items": items})


@require_POST
def add_to_cart(request):
    """
    Acepta:
      - content_type="catalog.product" y object_id, qty
      - type="product" | "mysterybox" y id, qty  (compatibilidad)
    """
    ct_key = (request.POST.get("content_type") or request.POST.get("type") or "").strip().lower()
    object_id = request.POST.get("object_id") or request.POST.get("id")
    qty_raw = request.POST.get("qty", "1")

    try:
        qty = max(1, int(qty_raw))
    except ValueError:
        qty = 1

    if not ct_key or not object_id:
        messages.error(request, "Faltan datos para agregar al carrito.")
        return redirect(request.META.get("HTTP_REFERER") or "orders:list")

    if ct_key in ("product", "catalog.product"):
        obj = get_object_or_404(Product, pk=object_id)
        price_field = "price_cop"
    elif ct_key in ("mysterybox", "mistery_boxes.mysterybox", "box"):
        if MysteryBox is None:
            messages.error(request, "El tipo MysteryBox aún no está disponible.")
            return redirect(request.META.get("HTTP_REFERER") or "orders:list")
        obj = get_object_or_404(MysteryBox, pk=object_id)
        price_field = "price_cop"
    else:
        messages.error(request, "Tipo de ítem inválido.")
        return redirect(request.META.get("HTTP_REFERER") or "orders:list")

    cart = get_or_create_cart(request)
    add_item(cart, obj, qty=qty, price_field=price_field)

    messages.success(request, "Producto agregado al carrito.")
    next_url = request.POST.get("next") or request.GET.get("next") \
               or request.META.get("HTTP_REFERER") or "orders:list"
    return redirect(next_url)


@require_POST
def update_quantity(request, item_id: int):
    """Actualiza cantidad SOLO si el item pertenece al carrito actual."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = item.quantity
    set_quantity(item, qty)
    messages.success(request, "Cantidad actualizada.")
    return redirect("orders:list")


@require_POST
def remove_from_cart(request, item_id: int):
    """Elimina item SOLO si pertenece al carrito actual."""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    remove_item(item)
    messages.info(request, "Ítem eliminado.")
    return redirect("orders:list")