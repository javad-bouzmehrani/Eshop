from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Slider


@admin.register(Slider)
class SliderAdmin(ModelAdmin):
    list_display = ("id", "title", "link")
    search_fields = ("title", "description", "link")
    ordering = ("id",)
    list_per_page = 20