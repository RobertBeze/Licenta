from django.urls import path, include, re_path
from . import views

urlpatterns=[
	path('inbox/',views.InboxView.as_view(), name='inbox'),
	re_path(r'^inbox/(?P<username>\w+)/$', views.InboxWithView.as_view(), name='direct-msg'),
]