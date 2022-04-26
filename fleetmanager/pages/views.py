from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserForm, UserPwd, DetaliuFoaieForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from vehicles.models import Vehicle
import datetime
from dateutil.relativedelta import relativedelta
from .models import FoaieParcurs, DetaliiFoaieParcurs

# Create your views here.
class HomeView(View):
	template_name = 'pages/default.html'

	def get_obj(self, request):
		obj = Vehicle.objects.filter(vehicle_driver=request.user)
		if not obj:
			return None
		else:
			return obj[0]

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return render(request, self.template_name)

		if request.user.is_superuser:
			self.template_name = 'pages/home_admin.html'
			today = datetime.date.today()
			month = today + relativedelta(months=1)
			itp_expirat = Vehicle.objects.filter(vehicle_itp__lte=today)
			itp_luna = Vehicle.objects.filter(vehicle_itp__lte=month).exclude(vehicle_itp__lte=today)
			rca_expirat = Vehicle.objects.filter(vehicle_rca__lte=today)
			rca_luna = Vehicle.objects.filter(vehicle_rca__lte=month).exclude(vehicle_rca__lte=today)
			context={
				'itp_expirat':itp_expirat,
				'itp_luna':itp_luna,
				'rca_expirat':rca_expirat,
				'rca_luna':rca_luna,
			}

			if not itp_expirat.exists():
				context['itp_expirat'] = None
			if not itp_luna.exists():
				context['itp_luna'] = None
			if not rca_expirat.exists():
				context['rca_expirat'] = None
			if not rca_luna.exists():
				context['rca_luna'] = None

			return render(request, self.template_name,context)

		context = {'vehicle' : self.get_obj(request)}
		self.template_name = 'pages/home.html'
		return render(request, self.template_name, context)


class UserCreateView(View):
	template_name = 'pages/create_user.html'

	def get(self, request, *args, **kwargs):
		form = UserForm()
		context ={
		'form':form,
		}

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = UserForm(request.POST)
		context ={
		'form':form,
		}
		if form.is_valid():
			form.save()
			return redirect('user-list')

		if not request.user.is_superuser:
			return redirect('home')
		return render(request, self.template_name, context)


class UserListView(View):
	template_name = 'pages/user_list.html'

	def get_queryset(self):
		return User.objects.all()

	def get(self, request, *args, **kwargs):
		if not request.user.is_superuser:
			return redirect('home')

		context = {'user_list':self.get_queryset()}
		return render(request, self.template_name, context)


class UserSearchView(View):
	template_name = 'pages/user_list_search.html'

	def post(self, request, *args, **kwargs):
		searched = request.POST['searched']
		usr = User.objects.filter(username__contains=searched)
		if usr.count() == 0:
			context = {'notfound': True}
		else:
			context = {'user_list':usr, 'searched':searched}
		return render(request, self.template_name, context)

	def get(self, request, *args, **kwargs):
		context = {'searched': False}
		return render(request, self.template_name, context)

class UserPwdView(View):
	template_name = 'pages/user_pwd.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(User, id=id)
		return obj

	def get(self, request, *args, **kwargs):
		obj = self.get_obj()
		form = UserPwd()
		context = {
			'form' : form,
			'user' : obj
		}

		if not request.user.is_superuser:
			return redirect('home')

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		obj = self.get_obj()
		form = UserPwd(request.POST)
		context = {
			'form' : form,
			'user' : obj
		}

		if not request.user.is_superuser:
			return redirect('home')

		if form.is_valid():
			pwd = form.cleaned_data.get('password1')
			obj.set_password(form.cleaned_data.get('password1'))
			obj.save()
			return redirect('user-list')

		return render(request, self.template_name, context)

class UserDelView(View):
	template_name = 'pages/user_delete.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(User, id=id)
		return obj

	def get(self, request, *args, **kwargs):
		context = {}
		obj = self.get_obj()
		if obj is not None:
			context['user'] = obj

		if not request.user.is_superuser:
			return redirect('home')

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context = {}
		obj = self.get_obj()

		if not request.user.is_superuser:
			return redirect('home')

		if obj is not None:
			obj.delete()
			context['user'] = None
			return redirect('user-list')

		return render(request, self.template_name, context)

class FoaieView(View): #lista foi vehicul
	template_name = 'pages/lista_foi_parcurs.html'
	def get(self, request):
		if not request.user.is_authenticated:
			return redirect('home')
		if request.user.is_superuser:
			return redirect('home')
		context = {}
		veh = Vehicle.objects.filter(vehicle_driver=request.user)
		if veh:
			lista_foi = FoaieParcurs.objects.filter(vehicle=veh[0])
			exists = True
		else:
			lista_foi = None
			exists = None
		context['foi'] = lista_foi
		context['exists'] = exists
		return render(request, self.template_name, context)

	def post(self,request):
		obj = get_object_or_404(Vehicle, vehicle_driver=request.user)
		foaie = FoaieParcurs(vehicle=obj, creation_date=datetime.date.today())
		foaie.save()
		return redirect('foaie-parcurs')


class FoaieDetaliuView(View):
	template_name = 'pages/foaie_detaliu.html'

	def get_obj(self):
		id = self.kwargs.get('id')
		obj = None
		if id != None:
			obj = get_object_or_404(FoaieParcurs, id=id)
		return obj

	def get(self,request,*args,**kwargs):
		foaie = self.get_obj()
		context={}
		context['foaie'] = foaie
		detalii = DetaliiFoaieParcurs.objects.filter(foaie=foaie)
		context['detalii'] = detalii

		return render(request, self.template_name, context)


class FoaieDetaliuAddView(View):
	template_name = 'pages/foaie_detaliu_add.html'
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('home')
		form = DetaliuFoaieForm()
		context = {}
		context['form'] = form
		return render(request, self.template_name,context)

	def post(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			return redirect('home')
		form = DetaliuFoaieForm(request.POST)

		context = {
			'form' : form,
		}

		if form.is_valid():
			arrival = form.cleaned_data.get('arrival')
			departure = form.cleaned_data.get('departure')
			date_departure = form.cleaned_data.get('date_departure')
			date_arrival = form.cleaned_data.get('date_arrival')
			km = form.cleaned_data.get('km')
			foaie = FoaieParcurs.objects.filter(id=self.kwargs.get('id'))
			if foaie:
				foaie = foaie[0]
				detaliu = DetaliiFoaieParcurs(foaie=foaie, departure=departure,arrival=arrival,date_departure=date_departure, date_arrival=date_arrival, km=km)
				detaliu.save()
				return redirect('foaie-detaliu', self.kwargs.get('id'))
		return render(request,self.template_name,context)
