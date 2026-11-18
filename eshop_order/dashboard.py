from django.utils import timezone
from datetime import timedelta


def dashboard_callback(request, context):
    from eshop_order.models import Order
    from eshop_products.models import product
    from eshop_tag.models import Tag

    last_week = timezone.now() - timedelta(days=7)

    context.update({
        "kpi_orders_total": Order.objects.count(),
        "kpi_orders_paid": Order.objects.filter(paid=True).count(),
        "kpi_orders_pending": Order.objects.filter(paid=False).count(),
        "kpi_orders_week": Order.objects.filter(id__gte=1).count(),
        "kpi_products_total": product.objects.count(),
        "kpi_products_active": product.objects.filter(active=True).count(),
        "kpi_products_featured": product.objects.filter(featured=True).count(),
        "kpi_tags_total": Tag.objects.count(),
        "recent_orders": Order.objects.select_related("user").order_by("-id")[:5],
    })

    return context