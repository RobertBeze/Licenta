from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.UserCreateView.as_view(), name='register-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:id>/change_pass', views.UserPwdView.as_view(), name='user-change-pass'),
    path('users/<int:id>/delete', views.UserDelView.as_view(), name='user-delete'),
    path('users/search_user', views.UserSearchView.as_view(), name='search-user'),
    path('parcurs/', views.FoaieView.as_view(), name='foaie-parcurs'), #lista foi parcurs pt un anumit vehicul
    path('parcurs/<int:id>', views.FoaieDetaliuView.as_view(), name = 'foaie-detaliu'), #pagina de detalii pentru foaia de parcurs
    path('parcurs/<int:id>/add', views.FoaieDetaliuAddView.as_view(), name='foaie-detaliu-add'), #adauga detalii
    path('detalii/<int:id>/update', views.DetaliiUpdateView.as_view(), name='detaliu-update'), #modifica detalii
    path('detalii/<int:id>/delete', views.DetaliiDeleteView.as_view(), name='detaliu-delete'), #sterge detalii

    path('parcurs/<int:id>/delete', views.FoaieRemoveView.as_view(), name='foaie-parcurs-delete'), #restricted for admin only, sterge foi de parcurs
    path('parcurs/<int:id>/extend', views.FoaieExtendView.as_view(), name='foaie-parcurs-extend'), #restricted for admin only, extinde perioada
]
