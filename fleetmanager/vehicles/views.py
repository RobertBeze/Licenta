from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CategoryForm, VehicleForm, VehicleUpdateForm
from .models import Category, Vehicle
from django.contrib.auth.models import User
from django.views import View
from pages.models import FoaieParcurs, DetaliiFoaieParcurs
import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser

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
			foi = FoaieParcurs.objects.filter(vehicle=vehicle)
			if foi:
				for f in foi:
					detalii= DetaliiFoaieParcurs.objects.filter(foaie=f)
					if detalii:
						for d in detalii:
							d.delete()
					f.delete()

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
		form = VehicleUpdateForm(instance = obj)
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


	def get(self, request, id, *args, **kwargs):
		context = {}
		if id != None:
			obj = get_object_or_404(Vehicle, id=id)
			context['vehicle'] = obj
		return render(request, self.template_name, context)


class VehicleListView(View):
	template_name = 'vehicles/vehicle_list.html'

	def get_queryset(self):
		return Vehicle.objects.all()

	def get(self, request, *args, **kwargs):
		context = {'vehicle_list':self.get_queryset()}
		return render(request, self.template_name, context)


class VehicleSearchView(View):
	template_name = 'vehicles/vehicle_list_search.html'

	def post(self, request, *args, **kwargs):
		searched = request.POST['searched']
		veh = Vehicle.objects.filter(vehicle_plate__contains=searched)
		if veh.count() == 0:
			context = {'notfound': True}
		else:
			context = {'vehicle_list':veh, 'searched':searched}
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		context = {'searched': False}
		return render(request, self.template_name, context)


class CategoryListView(View):
	template_name = 'vehicles/category_list.html'

	def get_queryset(self):
		return Category.objects.all()

	def get(self, request, *args, **kwargs):
		context = {'category_list': self.get_queryset()}
		return render(request, self.template_name, context)

class CategoryDeleteView(View):
	template_name = 'vehicles/category_delete.html'

	def get_category(self):
		id = self.kwargs.get('id')
		category = None
		if id is not None:
			category = get_object_or_404(Category, id=id)
		return category

	def get(self, request, id, *args, **kwargs):
		context = {}
		category = self.get_category()
		if category is not None:
			context['category'] = category

		if not request.user.is_superuser:
			return redirect('home')

		return render(request, self.template_name, context)

	def post(self, request, id, *args, **kwargs):
		context = {}
		category = self.get_category()

		if not request.user.is_superuser:
			return redirect('home')

		if category is not None:
			category.delete()
			context['category'] = None
			return redirect('category-list')
		return render(request, self.template_name, context)

class CategoryCreateView(View):
	template_name = 'vehicles/create_category.html'

	def get(self, request, *args, **kwargs):
		form = CategoryForm()
		context ={
		'form':form,
		}

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = CategoryForm(request.POST)
		context ={
		'form':form,
		}
		if form.is_valid():
			form.save()
			return redirect('category-list')

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)


class CategoryUpdateView(View):
	template_name = 'vehicles/category_update.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(Category, id=id)
		return obj


	def get(self, request, *args, **kwargs):
		obj = self.get_obj()
		form = CategoryForm(instance = obj)
		context ={
		'form':form,
		'category' : obj
		}

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		obj = self.get_obj()
		form = CategoryForm(request.POST, instance = obj)
		context ={
		'form':form,
		'category' : obj
		}
		if form.is_valid():
			form.save()
			return redirect('category-list')

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)



class VehicleParcursView(View):
	template_name = 'vehicles/lista_foi_parcurs.html'
	def get(self,request,*args,**kwargs):
		id = self.kwargs.get('id')
		veh = Vehicle.objects.get(id=id)
		foi = FoaieParcurs.objects.filter(vehicle=veh)

		for f in foi:
			if f.data_expirare < datetime.date.today():
				f.expired = True
				f.save()

		context = {
			'foi' : foi,
		}

		return render(request,self.template_name,context)

	def post(self,request, *args, **kwargs):
		id = self.kwargs.get('id')
		obj = get_object_or_404(Vehicle, id=id)
		expire = datetime.date.today() + relativedelta(days=5)
		foaie = FoaieParcurs(vehicle=obj, creation_date=datetime.date.today(), data_expirare=expire)
		foaie.save()
		return redirect('vehicle-parcurs', id)

class ProceseazaFoiParcurs(View):
	def get(self, request, *args, **kwargs):
		foi = FoaieParcurs.objects.all()
		for f in foi:
			if f.data_expirare < datetime.date.today():
				f.expired = True
				f.save()
		for f in foi:
			if f.expired:
				if not f.procesat:
					detalii = DetaliiFoaieParcurs.objects.filter(foaie=f)
					veh = f.vehicle
					for d in detalii:
						km = d.km
						veh.vehicle_odometer = veh.vehicle_odometer + km
					veh.save()
					f.procesat = True
					f.save()
		return redirect('vehicle-list')


class TopKMView(View):
	template_name = 'vehicles/top_km.html'
	def get(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return redirect('home')

		data = {}
		start_date = datetime.date.today() - relativedelta(months=1)
		end_date = datetime.date.today()
		am_ceva = False
		lista_foi = FoaieParcurs.objects.filter(procesat=True)
		for foaie in lista_foi:
			if start_date <= foaie.creation_date <= end_date:
				am_ceva = True
				veh = foaie.vehicle
				km = 0
				detalii = DetaliiFoaieParcurs.objects.filter(foaie=foaie)
				if detalii:
					for d in detalii:
						km = km + d.km
					data[veh.vehicle_plate] = km

		if am_ceva:
			data_sorted = sorted(data.items(), key=lambda x: x[1], reverse=True)
		else:
			data_sorted = False
		context = { 'data' : data_sorted}
		return render(request,self.template_name,context)

class TopKMSearchView(View):
	template_name = 'vehicles/top_km_s.html'

	def post(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return redirect('home')

		data = {}

		start_date = parser.parse(request.POST['fdata'])
		start_date = start_date.date()
		#start_date = datetime.date.today() - relativedelta(months=1)
		end_date = parser.parse(request.POST['ldata'])
		end_date = end_date.date()
		#end_date = datetime.date.today()
		if start_date > end_date:
			tmp = end_date
			end_date = start_date
			start_date = tmp

		am_ceva = False
		lista_foi = FoaieParcurs.objects.filter(procesat=True)
		for foaie in lista_foi:
			if start_date <= foaie.creation_date <= end_date:
				am_ceva = True
				veh = foaie.vehicle
				km = 0
				detalii = DetaliiFoaieParcurs.objects.filter(foaie=foaie)
				if detalii:
					for d in detalii:
						km = km + d.km
					data[veh.vehicle_plate] = km

		if am_ceva:
			data_sorted = sorted(data.items(), key=lambda x: x[1], reverse=True)
		else:
			data_sorted = False
		context = { 'data' : data_sorted, 'fdata': start_date, 'ldata': end_date, 'searched': True}
		return render(request,self.template_name,context)

	def get(self, request, *args, **kwargs):
		context = {'searched': False}
		return render(request, self.template_name, context)