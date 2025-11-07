from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from catalog.models import Product
from mistery_boxes.models import MysteryBox
from django.contrib.auth.models import User


@staff_member_required
def admin_dashboard(request):
    """
    Dashboard principal de administración con estadísticas generales.
    Solo accesible para staff/administradores.
    """
    # Período de tiempo seleccionado
    period = request.GET.get('period', '30')  # Días por defecto
    try:
        days = int(period)
    except ValueError:
        days = 30
    
    start_date = timezone.now() - timedelta(days=days)
    
    # Estadísticas generales
    total_sales = Order.objects.filter(
        status='paid',
        created_at__gte=start_date
    ).aggregate(total=Sum('total_cop'))['total'] or 0
    
    total_orders = Order.objects.filter(
        status='paid',
        created_at__gte=start_date
    ).count()
    
    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte=start_date).count()
    
    # Productos más vendidos
    top_products = OrderItem.objects.filter(
        order__status='paid',
        order__created_at__gte=start_date,
        is_mystery_box=False
    ).values(
        'name'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('unit_price_cop'))
    ).order_by('-total_sold')[:10]
    
    # Mystery boxes más vendidas
    top_boxes = OrderItem.objects.filter(
        order__status='paid',
        order__created_at__gte=start_date,
        is_mystery_box=True
    ).values(
        'name'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('unit_price_cop'))
    ).order_by('-total_sold')[:10]
    
    # Ventas por día (últimos días del período)
    sales_by_day = Order.objects.filter(
        status='paid',
        created_at__gte=start_date
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        total=Sum('total_cop'),
        count=Count('id')
    ).order_by('day')
    
    # Productos ganados en mystery boxes (más populares)
    top_won_products = OrderItem.objects.filter(
        order__status='paid',
        order__created_at__gte=start_date,
        is_mystery_box=True,
        won_product__isnull=False
    ).values(
        'won_product__name'
    ).annotate(
        times_won=Count('id')
    ).order_by('-times_won')[:10]
    
    context = {
        'period': days,
        'start_date': start_date,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_users': total_users,
        'new_users': new_users,
        'top_products': top_products,
        'top_boxes': top_boxes,
        'sales_by_day': sales_by_day,
        'top_won_products': top_won_products,
        'avg_order_value': total_sales / total_orders if total_orders > 0 else 0,
    }
    
    return render(request, 'admin/dashboard.html', context)


@staff_member_required
def sales_report(request):
    """
    Reporte detallado de ventas.
    Solo accesible para staff/administradores.
    """
    # Período de tiempo
    period = request.GET.get('period', '30')
    try:
        days = int(period)
    except ValueError:
        days = 30
    
    start_date = timezone.now() - timedelta(days=days)
    
    # Todas las órdenes del período
    orders = Order.objects.filter(
        status='paid',
        created_at__gte=start_date
    ).select_related('user').prefetch_related('items').order_by('-created_at')
    
    # Estadísticas
    total_revenue = orders.aggregate(total=Sum('total_cop'))['total'] or 0
    total_orders_count = orders.count()
    
    # Ventas por categoría (aproximado usando productos)
    category_sales = OrderItem.objects.filter(
        order__status='paid',
        order__created_at__gte=start_date
    ).values(
        'is_mystery_box'
    ).annotate(
        total=Sum(F('quantity') * F('unit_price_cop')),
        count=Sum('quantity')
    )
    
    context = {
        'period': days,
        'start_date': start_date,
        'orders': orders[:50],  # Limitar a 50 para no sobrecargar
        'total_revenue': total_revenue,
        'total_orders_count': total_orders_count,
        'category_sales': category_sales,
        'avg_order': total_revenue / total_orders_count if total_orders_count > 0 else 0,
    }
    
    return render(request, 'admin/sales_report.html', context)


@staff_member_required
def user_report(request):
    """
    Reporte de usuarios registrados.
    Solo accesible para staff/administradores.
    """
    # Filtros
    search = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '-date_joined')
    
    users = User.objects.all()
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Anotar con número de órdenes y total gastado
    users = users.annotate(
        total_orders=Count('order', filter=Q(order__status='paid')),
        total_spent=Sum('order__total_cop', filter=Q(order__status='paid'))
    ).order_by(order_by)
    
    # Estadísticas generales
    total_users = User.objects.count()
    active_buyers = User.objects.filter(order__status='paid').distinct().count()
    this_month_users = User.objects.filter(
        date_joined__gte=timezone.now().replace(day=1)
    ).count()
    
    context = {
        'users': users[:100],  # Limitar a 100
        'search': search,
        'order_by': order_by,
        'total_users': total_users,
        'active_buyers': active_buyers,
        'this_month_users': this_month_users,
    }
    
    return render(request, 'admin/user_report.html', context)
