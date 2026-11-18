from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product_category


@admin.register(Product_category)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ("id", "title", "name")
    search_fields = ("title", "name")
    ordering = ("id",)
    list_per_page = 20
    list_editable = ("name",)