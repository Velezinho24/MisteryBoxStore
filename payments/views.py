from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from orders.models import Order, OrderItem
from orders.services import get_or_create_cart
from .models import PaymentTransaction
from .utils import generate_invoice_pdf

USE_DUMMY = getattr(settings, "USE_DUMMY_PAYMENTS", True)
DUMMY_GATEWAY = getattr(settings, "DUMMY_GATEWAY_NAME", "dummy")

def _build_order_from_cart(request):
    """
    Crea Order y OrderItems a partir del carrito activo.
    Devuelve (order, cart). Si el carrito está vacío, devuelve (None, cart).
    """
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related("content_type"))
    if not items:
        return None, cart

    email = request.user.email if request.user.is_authenticated else "guest@example.com"
    total = sum(int(i.quantity) * int(i.unit_price_snapshot) for i in items)

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
        total_cop=int(total),
        status="pending",
    )
    for it in items:
        OrderItem.objects.create(
            order=order,
            name=getattr(it.content_object, "name", f"Item {it.id}"),
            quantity=int(it.quantity),
            unit_price_cop=int(it.unit_price_snapshot),
            line_total_cop=int(it.line_total),
        )
    return order, cart

def checkout_start(request):
    """
    Si USE_DUMMY=True (Sprint 01): renderiza un checkout simulado.
    Si USE_DUMMY=False: aquí conectarás Stripe Checkout en el Sprint 02.
    """
    order, cart = _build_order_from_cart(request)
    if not order:
        return redirect("orders:cart_detail")

    if USE_DUMMY:
        return render(request, "payments/checkout.html", {"order": order})
    else:
        return render(request, "payments/checkout.html", {"order": order})


def checkout_confirm_dummy(request, order_id: int):
    """
    Confirma pago ficticio: marca la orden como paid, crea PaymentTransaction,
    genera PDF y redirige a success.
    """
    try:
        order = Order.objects.get(id=order_id, status="pending")
    except Order.DoesNotExist:
        return redirect("orders:cart_detail")

    PaymentTransaction.objects.create(
        order=order,
        gateway=DUMMY_GATEWAY,
        status="succeeded",
        external_id=f"dummy-{order.id}",
        amount_cop=order.total_cop,
        currency="COP",
    )

    order.status = "paid"
    order.save(update_fields=["status"])

    pdf_path = generate_invoice_pdf(order)
    rel = Path(pdf_path).relative_to(settings.MEDIA_ROOT)
    order.pdf_invoice.name = str(rel).replace("\\", "/")
    order.save(update_fields=["pdf_invoice"])

    return redirect(reverse("payments:checkout_success") + f"?order_id={order.id}")


def checkout_success(request):
    order_id = request.GET.get("order_id")
    return render(request, "payments/success.html", {"order_id": order_id})


def checkout_cancel(request):
    order_id = request.GET.get("order_id")
    return render(request, "payments/cancel.html", {"order_id": order_id})

@csrf_exempt
def stripe_webhook(request):
    """
    Definimos el webhook siempre para que exista la vista.
    - En modo dummy (Sprint 01) simplemente devolvemos 200.
    - Cuando pases a Stripe real (USE_DUMMY=False) aquí validas la firma
      y marcas órdenes como pagadas desde el evento de Stripe.
    """
    if USE_DUMMY:
        return HttpResponse(status=200)
    try:
        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        return HttpResponseBadRequest(str(e))

    return HttpResponse(status=200)