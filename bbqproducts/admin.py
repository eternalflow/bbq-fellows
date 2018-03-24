from django.contrib import admin
from .models import BBQProduct


@admin.register(BBQProduct)
class BBQProductAdmin(admin.ModelAdmin):
    pass
