"""
URL configuration for MisteryBoxStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from orders.views import cart_detail
from .admin_views import admin_dashboard, sales_report, user_report

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # set_language
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("", include(("MisteryBoxStore.home_urls", "home"), namespace="home")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("catalog/", include(("catalog.urls", "catalog"), namespace="catalog")),
    path("mistery-boxes/", include(("mistery_boxes.urls", "mistery_boxes"), namespace="mistery_boxes")),
    path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),
    path("cart/", cart_detail, name="cart_root"),
    # Admin Reports
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-reports/sales/", sales_report, name="sales_report"),
    path("admin-reports/users/", user_report, name="user_report"),
)


urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # only for development environment
