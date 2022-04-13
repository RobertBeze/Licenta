from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserForm, UserPwd, VehicleAddKMForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from vehicles.models import Vehicle

# Create your views here.
class HomeView(View):
	template_name = 'pages/default.html'

	def get_obj(self, request):
		obj = get_object_or_404(Vehicle, vehicle_driver=request.user)
		return obj

	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return render(request, self.template_name)

		if request.user.is_superuser:
			self.template_name = 'pages/home_admin.html'
			return render(request, self.template_name)

		context = {'vehicle' : self.get_obj(request)}
		self.template_name = 'pages/home.html'
		return render(request, self.template_name, context)

class AdKM(View):
	template_name = 'pages/driver_add_km.html'

	def get_obj(self,request):
		return get_object_or_404(Vehicle, vehicle_driver=request.user)

	def get(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			return redirect('home')
		form = VehicleAddKMForm()
		context = {
			'form':form,
		}
		return render(request, self.template_name,context)

	def post(self,request,*args,**kwargs):
		if not request.user.is_authenticated:
			return redirect('home')
		form = VehicleAddKMForm(request.POST)
		context = {'form' : form}
		if form.is_valid():
			km = form.cleaned_data.get('vehicle_odometer')
			obj = self.get_obj(request)
			obj.vehicle_odometer += km
			obj.save()
			return redirect('home')
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

