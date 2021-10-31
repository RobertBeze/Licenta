from django.urls import path, include
from . import views

urlpatterns = [
    path('create_category/',views.create_category, name='create-category'),
    path('create_vehicle/',views.VehicleCreateView.as_view(), name='create-vehicle'),
    path('vehicle_list/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('<int:id>/', views.VehicleView.as_view(), name='vehicle-detail-view'),
    path('<int:id>/delete', views.VehicleDeleteView.as_view(), name='vehicle-delete-view')
]
