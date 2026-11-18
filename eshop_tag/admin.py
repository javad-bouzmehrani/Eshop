from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "active", "timestamp")
    list_filter = ("active", "timestamp")
    search_fields = ("title", "slug")
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"
    list_per_page = 20
    list_editable = ("active",)
    readonly_fields = ("slug", "timestamp")
    filter_horizontal = ("products",)