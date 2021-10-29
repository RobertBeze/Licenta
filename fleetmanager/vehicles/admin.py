from django.contrib import admin

# Register your models here.
from .models import Category, Vehicle
admin.site.register(Category)
admin.site.register(Vehicle)