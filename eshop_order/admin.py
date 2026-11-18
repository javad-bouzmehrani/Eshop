from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "count", "price", "total_price_display")
    readonly_fields = ("total_price_display",)

    @admin.display(description="جمع ردیف")
    def total_price_display(self, obj):
        if obj.pk:
            return obj.total_price()
        return "—"


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        "id",
        "user",
        "paid",
        "pay_date",
        "subtotal_display",
        "discount_display",
        "total_display",
    )
    list_filter = ("paid", "pay_date")
    search_fields = (
        "id",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("-id",)
    date_hierarchy = "pay_date"
    list_per_page = 20
    inlines = (OrderItemInline,)
    list_select_related = ("user",)
    readonly_fields = ("pay_date",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("orderitem_set__product")

    @admin.display(description="جمع قبل از تخفیف")
    def subtotal_display(self, obj):
        return obj.subtotal()

    @admin.display(description="تخفیف")
    def discount_display(self, obj):
        return obj.discount()

    @admin.display(description="قابل پرداخت")
    def total_display(self, obj):
        return obj.total()


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ("id", "order", "product", "count", "price", "total_price_display")
    list_filter = ("order__paid",)
    search_fields = ("order__id", "product__title")
    list_select_related = ("order", "product")

    @admin.display(description="جمع")
    def total_price_display(self, obj):
        return obj.total_price()