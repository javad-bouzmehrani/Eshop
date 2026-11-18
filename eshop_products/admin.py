from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import product, Product_gallery


class ProductGalleryInline(TabularInline):
    model = Product_gallery
    extra = 0
    fields = ("title", "image")


@admin.register(product)
class ProductAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "old_price",
        "discount",
        "active",
        "featured",
        "offer",
        "visits",
        "time",
    )
    list_filter = ("active", "featured", "offer", "cetegories", "time")
    search_fields = ("title", "description")
    ordering = ("-time",)
    date_hierarchy = "time"
    list_per_page = 20
    list_editable = ("active", "featured", "offer")
    filter_horizontal = ("cetegories",)
    inlines = (ProductGalleryInline,)
    readonly_fields = ("visits", "time")


@admin.register(Product_gallery)
class ProductGalleryAdmin(ModelAdmin):
    list_display = ("id", "title", "product")
    list_filter = ("product",)
    search_fields = ("title", "product__title")
    ordering = ("-id",)
    list_per_page = 20
    list_select_related = ("product",)