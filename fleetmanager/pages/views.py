from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home_view(request):
	#print(request.user)
	#print(request.user.is_authenticated)
	if not request.user.is_authenticated:
		return render(request, "pages/default.html")

	if request.user.is_superuser:
		return render(request, "pages/home_admin.html", {})
	return render(request, "pages/home.html", {})
