from django.urls import path, include
from . import views

urlpatterns = [
    path('create_category/',views.CategoryCreateView.as_view(), name='create-category'),
    path('create_vehicle/',views.VehicleCreateView.as_view(), name='create-vehicle'),
    path('vehicle_list/', views.VehicleListView.as_view(), name='vehicle-list'),
    path('<int:id>/', views.VehicleView.as_view(), name='vehicle-detail-view'),
    path('<int:id>/delete', views.VehicleDeleteView.as_view(), name='vehicle-delete-view'),
    path('<int:id>/update', views.VehicleUpdateView.as_view(), name='vehicle-update-view'),
    path('<int:id>/parcurs', views.VehicleParcursView.as_view(), name='vehicle-parcurs'),
    path('category_list/', views.CategoryListView.as_view(), name='category-list'),
    path('category_list/<int:id>/delete', views.CategoryDeleteView.as_view(), name='category-delete-view'),
    path('category_list/<int:id>/update', views.CategoryUpdateView.as_view(), name='category-update-view'),
    path('category_list/<int:id>/', views.CategoryListView.as_view(), name='category-view'),
    path('search_vehicle/', views.VehicleSearchView.as_view(), name='search-vehicle'),
    path('parcurs/', views.ProceseazaFoiParcurs.as_view(),name='proceseaza-foi'),
    #path('topkm/', views.TopKMView().as_view(), name='top-km'),
]
