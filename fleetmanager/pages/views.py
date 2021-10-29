from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home_view(request):
	#print(request.user)
	#print(request.user.is_authenticated)
	return render(request, "home.html", {})
