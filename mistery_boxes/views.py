from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import MysteryBox
from .forms import MysteryBoxForm
from orders.models import Order, OrderItem
from catalog.models import Product


@login_required
def mysterybox_list(request):
    boxes = MysteryBox.objects.filter(is_active=True).prefetch_related('products')
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
    
    # Calcular estadísticas
    total_value = sum(p.price_cop for p in products)
    savings = total_value - box.price_cop
    savings_percentage = (savings / total_value * 100) if total_value > 0 else 0

    return render(request, "mysteryboxes/box_detail.html", {
        "box": box,
        "products": products,
        "total_value": total_value,
        "savings": savings,
        "savings_percentage": savings_percentage,
    })


@login_required
@require_POST
def buy_mystery_box(request, box_id):
    """
    Compra directa de una mystery box (sin pasar por carrito).
    Crea la orden y redirige al checkout simulado.
    """
    box = get_object_or_404(MysteryBox, id=box_id, is_active=True)
    
    # Crear la orden directamente
    email = request.user.email if request.user.is_authenticated else "guest@example.com"
    
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=email,
        total_cop=int(box.price_cop),
        status="pending",
    )
    
    # Crear OrderItem marcado como mystery box
    OrderItem.objects.create(
        order=order,
        name=box.name,
        quantity=1,
        unit_price_cop=int(box.price_cop),
        line_total_cop=int(box.price_cop),
        is_mystery_box=True,
        mystery_box_id=box.id,
    )
    
    messages.success(request, f"Mystery Box '{box.name}' añadida a tu orden!")
    
    # Redirigir al checkout (que luego redirigirá a la página de reveal)
    return redirect(reverse('payments:checkout_start_box', kwargs={'order_id': order.id}))


@login_required
def mystery_box_reveal(request):
    """
    Página de revelación del producto ganado en una mystery box.
    Muestra animación y el producto final.
    """
    order_id = request.GET.get("order_id")
    if not order_id:
        messages.error(request, "No se encontró la orden")
        return redirect("mystery_boxes:list")
    
    try:
        order = Order.objects.get(id=order_id, status="paid")
    except Order.DoesNotExist:
        messages.error(request, "Orden no encontrada o no pagada")
        return redirect("mystery_boxes:list")
    
    # Verificar que el usuario tenga permiso
    if order.user and order.user != request.user:
        messages.error(request, "No tienes permiso para ver esta orden")
        return redirect("mystery_boxes:list")
    
    # Obtener los items de mystery box con sus productos ganados
    mystery_box_items = order.items.filter(is_mystery_box=True, won_product__isnull=False)
    
    if not mystery_box_items.exists():
        messages.error(request, "No se encontraron mystery boxes en esta orden")
        return redirect("mystery_boxes:list")
    
    # Tomar el primer item (asumimos una mystery box por orden en compra directa)
    item = mystery_box_items.first()
    won_product = item.won_product
    
    # Obtener la mystery box original para mostrar información
    try:
        mystery_box = MysteryBox.objects.get(id=item.mystery_box_id)
        all_possible_products = list(mystery_box.products.all())
    except MysteryBox.DoesNotExist:
        mystery_box = None
        all_possible_products = []
    
    return render(request, "mysteryboxes/reveal.html", {
        "order": order,
        "item": item,
        "won_product": won_product,
        "mystery_box": mystery_box,
        "all_possible_products": all_possible_products,
    })
