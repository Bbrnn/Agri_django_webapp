from django.contrib import admin

from products.models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
    search_fields = ("name",)
    list_filter = ("updated_at",)
    ordering = ("-updated_at",)#show latest products first
