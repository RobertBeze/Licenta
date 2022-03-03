from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home_view, name='home'),
    path('register/', views.UserCreateView.as_view(), name='register-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:id>/change_pass', views.UserPwdView.as_view(), name='user-change-pass'),
    path('users/<int:id>/delete', views.UserDelView.as_view(), name='user-delete'),
    path('users/search_user', views.UserSearchView.as_view(), name='search-user'),
]
