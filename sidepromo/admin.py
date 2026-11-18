from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Slider, Promo


@admin.register(Slider)
class SideSliderAdmin(ModelAdmin):
    list_display = ("id", "title", "link")
    search_fields = ("title", "description", "link")
    ordering = ("id",)
    list_per_page = 20


@admin.register(Promo)
class PromoAdmin(ModelAdmin):
    list_display = ("id", "title", "tag", "description")
    search_fields = ("title", "tag", "description")
    ordering = ("id",)
    list_per_page = 20

    def has_add_permission(self, request):
        if Promo.objects.count() >= Promo.MAX_COUNT:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if Promo.objects.count() <= Promo.MAX_COUNT:
            return False
        return super().has_delete_permission(request, obj)