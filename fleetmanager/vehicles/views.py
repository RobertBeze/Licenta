from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CategoryForm, VehicleForm, VehicleUpdateForm
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

		if not request.user.is_superuser:
			return redirect('home')

		return render(request, self.template_name, context)

	def post(self, request, id, *args, **kwargs):
		context = {}
		vehicle = self.get_vehicle()

		if not request.user.is_superuser:
			return redirect('home')

		if vehicle is not None:
			vehicle.delete()
			context['vehicle'] = None
			return redirect('vehicle-list')

		return render(request, self.template_name, context)



class VehicleUpdateView(View):
	template_name = 'vehicles/update_vehicle.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(Vehicle, id=id)
		return obj


	def get(self, request, *args, **kwargs):
		obj = self.get_obj()
		driver = category = None
		if obj.vehicle_driver is not None:
			driver = obj.vehicle_driver

		if obj.vehicle_category is not None:
			category = obj.vehicle_category
		form = VehicleUpdateForm(instance = obj) #, initial={'vehicle_driver' : driver, 'vehicle_category' : category})
		context ={
		'form':form,
		'vehicle' : obj
		}

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		obj = self.get_obj()
		form = VehicleUpdateForm(request.POST, instance = obj)
		context ={
		'form':form,
		'vehicle' : obj
		}
		if form.is_valid():
			form.save()
			return redirect('vehicle-detail-view', self.kwargs.get('id'))

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)




class VehicleCreateView(View):
	template_name = 'vehicles/create_vehicle.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(Vehicle, id=id)
		return obj


	def get(self, request, *args, **kwargs):
		form = VehicleForm()
		context ={
		'form':form,
		}

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = VehicleForm(request.POST)
		context ={
		'form':form,
		}
		if form.is_valid():
			form.save()
			obj = get_object_or_404(Vehicle, vehicle_plate = form.cleaned_data['vehicle_plate'])
			return redirect('vehicle-detail-view',obj.id)

		if not request.user.is_superuser:
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

	if not request.user.is_superuser:
			return redirect('home')

	if form.is_valid():
		form.save();
		form = CategoryForm()
		return redirect('home')

	context = {
		'form':form
	}
	return render(request, 'vehicles/create_category.html', context)

