from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CategoryForm, VehicleForm
from .models import Category, Vehicle
from django.contrib.auth.models import User
from django.views import View

# Create your views here.


class VehicleDeleteView(View):
	template_name = 'vehicles/vehicle_delete.html'

	def get_vehicle(self):
		id = self.kwargs.get('id')
		vehicle = None
		if id is not None:
			vehicle = get_object_or_404(Vehicle, id=id)
		return vehicle

	def get(self, request, id, *args, **kwargs):
		context = {}
		vehicle = self.get_vehicle()
		if vehicle is not None:
			context['vehicle'] = vehicle
		return render(request, self.template_name, context)

	def post(self, request, id, *args, **kwargs):
		context = {}
		vehicle = self.get_vehicle()
		if vehicle is not None:
			vehicle.delete()
			context['vehicle'] = None
			return redirect('vehicle-list')
		return render(request, self.template_name, context)




class VehicleCreateView(View):
	template_name = 'vehicles/create_vehicle.html'

	def get_lista_categorii(self):
		return Category.objects.exclude(category_name='NONE')

	def get_lista_useri(self):
		return User.objects.exclude(username='NONE')

	def get(self, request, *args, **kwargs):
		form = VehicleForm()
		context ={
		'form':form,
		'category_list': self.get_lista_categorii(),
		'user_list': self.get_lista_useri()
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = VehicleForm(request.POST)
		context ={
		'form':form,
		'category_list': self.get_lista_categorii(),
		'user_list': self.get_lista_useri()
		}
		if form.is_valid():
			form.save()
			return redirect('home')
		return render(request, self.template_name, context)


class VehicleView(View):
	template_name = 'vehicles/vehicle_detail.html'


	def get(self, request, id, *arg, **kwargs):
		context = {}
		if id != None:
			obj = get_object_or_404(Vehicle, id=id)
			context['vehicle'] = obj
		return render(request, self.template_name, context)


class VehicleListView(View):
	template_name = 'vehicles/vehicle_list.html'

	def get_queryset(self):
		return Vehicle.objects.all()

	def get(self, request, *arg, **kwargs):
		context = {'vehicle_list':self.get_queryset()}
		return render(request, self.template_name, context)

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
