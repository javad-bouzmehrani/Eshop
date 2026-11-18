from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Setting


@admin.register(Setting)
class SettingAdmin(ModelAdmin):
    list_display = (
        "id",
        "site_name",
        "phone_support",
        "tag_up_left",
        "tag_up_right",
    )
    search_fields = (
        "site_name",
        "phone_support",
        "tag_up_left",
        "tag_up_right",
    )
    ordering = ("id",)
    list_per_page = 20