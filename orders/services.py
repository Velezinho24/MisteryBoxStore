from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import Cart, CartItem

SESSION_CART_KEY = "cart_id"

def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.create()

def get_or_create_cart(request):
    """
    1) Si hay cart_id en sesión -> úsalo.
    2) Si el usuario está logueado y tiene carrito -> úsalo.
    3) Si no, crea uno y guarda cart_id en sesión.
    """
    _ensure_session_key(request)

    cart = None
    cart_id = request.session.get(SESSION_CART_KEY)
    if cart_id:
        cart = Cart.objects.filter(id=cart_id).first()

    if request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user).order_by("-updated_at").first()
        if user_cart:
            cart = user_cart
            request.session[SESSION_CART_KEY] = cart.id

    if not cart:
        cart = Cart.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
        )
        request.session[SESSION_CART_KEY] = cart.id

    if request.user.is_authenticated and cart.user is None:
        cart.user = request.user
        cart.save(update_fields=["user", "updated_at"])

    return cart

@transaction.atomic
def add_item(cart, obj, qty: int = 1, price_field: str = "price_cop"):
    ct = ContentType.objects.get_for_model(obj.__class__)
    item = CartItem.objects.filter(cart=cart, content_type=ct, object_id=obj.id).first()
    unit_price = getattr(obj, price_field, None)
    if unit_price is None:
        raise AttributeError(f"No se encontró el campo de precio '{price_field}' en {obj.__class__.__name__}")

    if item:
        item.quantity += qty
        item.unit_price_snapshot = unit_price
        item.save(update_fields=["quantity", "unit_price_snapshot"])
    else:
        CartItem.objects.create(
            cart=cart,
            content_type=ct,
            object_id=obj.id,
            quantity=max(1, qty),
            unit_price_snapshot=unit_price,
        )
    return cart

@transaction.atomic
def set_quantity(cart_item: CartItem, qty: int):
    if qty <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save(update_fields=["quantity"])

@transaction.atomic
def remove_item(cart_item: CartItem):
    cart_item.delete()