from django.urls import path, include
from . import views

urlpatterns = [
    path('create_category/',views.create_category, name='create-category'),
    path('create_vehicle/',views.create_vehicle, name='create_vehicle'),
]
