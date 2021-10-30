from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CategoryForm, VehicleForm
from .models import Category
from django.contrib.auth.models import User

# Create your views here.


def create_category(request):
	form = CategoryForm(request.POST or None)
	if form.is_valid():
		form.save();
		form = CategoryForm()
		return redirect('home')

	context = {
		'form':form
	}
	return render(request, 'vehicles/create_category.html', context)


def create_vehicle(request):
	lista_categorii = Category.objects.exclude(category_name='NONE')
	lista_useri = User.objects.exclude(username='NONE')



	form = VehicleForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('home')

	context ={
		'form':form,
		'category_list': lista_categorii,
		'user_list': lista_useri
	}
	return render(request, 'vehicles/create_vehicle.html',context)
