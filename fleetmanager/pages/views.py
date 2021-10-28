from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_view(request):
	#print(request.user)
	#print(request.user.is_authenticated)
	return render(request, "home.html", {})