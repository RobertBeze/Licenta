from django.contrib import admin

# Register your models here.
from .models import FoaieParcurs, DetaliiFoaieParcurs
admin.site.register(FoaieParcurs)
admin.site.register(DetaliiFoaieParcurs)