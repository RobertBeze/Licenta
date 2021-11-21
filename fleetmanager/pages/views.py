from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserForm, UserPwd
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

def home_view(request):
	#print(request.user)
	#print(request.user.is_authenticated)
	if not request.user.is_authenticated:
		return render(request, "pages/default.html")

	if request.user.is_superuser:
		return render(request, "pages/home_admin.html", {})
	return render(request, "pages/home.html", {})


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

