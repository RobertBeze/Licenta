from django import forms
from .models import Category, Vehicle
from datetime import date
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class VehicleForm(forms.ModelForm):
	vehicle_plate = forms.CharField(label='Numărul înmatriculare')
	vehicle_odometer = forms.IntegerField(label='Kilometraj')
	vehicle_itp = forms.DateField(label='ITP expiră la')
	vehicle_rca = forms.DateField(label='RCA expiră la')
	vehicle_last_service = forms.IntegerField(label='KM ultima revizie')
	vehicle_driver = forms.CharField(label='Șofer', required=False)
	vehicle_category = forms.CharField(label='Categoria', required=False)

	class Meta:
		model = Vehicle
		fields = [
			'vehicle_plate',
			'vehicle_odometer',
			'vehicle_itp',
			'vehicle_rca',
			'vehicle_last_service',
			'vehicle_driver',
			'vehicle_category' 
		]

	def clean_vehicle_plate(self, *args, **kwargs):
		vehicle_plate = self.cleaned_data.get('vehicle_plate')
		obj_list = Vehicle.objects.all()
		for obj in obj_list:
			if vehicle_plate.lower() == obj.vehicle_plate.lower():
				raise forms.ValidationError("Acest număr de înmatriculare se află deja în baza de date!")
		if not vehicle_plate.isalnum():
			raise forms.ValidationError("Numărul de înmatriculare trebuie să conțină doar cifre și litere!")

		if len(vehicle_plate) > 7:
			raise forms.ValidationError("Lungimea maximă este de 7 caractere!")

		return vehicle_plate.upper()

	def clean_vehicle_odometer(self, *args, **kwargs):
		vehicle_odometer = self.cleaned_data.get('vehicle_odometer')
		if not isinstance(vehicle_odometer, int):
			raise forms.ValidationError("Doar cifre!")
		if vehicle_odometer < 0:
			raise forms.ValidationError("Doar numere pozitive")
		return vehicle_odometer

	def clean_vehicle_itp(self, *args, **kwargs):
		vehicle_itp = self.cleaned_data.get('vehicle_itp')
		current_date = date.today()

		if vehicle_itp < current_date:
			raise forms.ValidationError("Data nu este validă! Selectați o dată începând cu ziua curentă!")

		if not isinstance(vehicle_itp, date):
			raise forms.ValidationError("Aceasta nu este o dată!")

		return vehicle_itp

	def clean_vehicle_rca(self, *args, **kwargs):
		vehicle_rca = self.cleaned_data.get('vehicle_rca')
		current_date = date.today()

		if vehicle_rca < current_date:
			raise forms.ValidationError("Data nu este validă! Selectați o dată începând cu ziua curentă!")

		if not isinstance(vehicle_rca, date):
			raise forms.ValidationError("Aceasta nu este o dată!")

		return vehicle_rca

	def clean_vehicle_last_service(self, *args, **kwargs):
		vehicle_last_service = self.cleaned_data.get('vehicle_last_service')
		vehicle_odometer = self.cleaned_data.get('vehicle_odometer')
		if not isinstance(vehicle_last_service, int):
			raise forms.ValidationError("Doar cifre!")
		if vehicle_last_service > vehicle_odometer:
			raise forms.ValidationError("KM de la ultima revizie trebuie să fie mai mici decât kilometrajul actual!")
		return vehicle_last_service

	def clean_vehicle_driver(self, *args, **kwargs):
		vehicle_driver = self.cleaned_data.get('vehicle_driver')
		user_list = User.objects.all()
		k = 0

		if not vehicle_driver:
			return User.objects.get(username='NONE')

		for user in user_list:
			if vehicle_driver.lower() == user.get_username().lower():
				my_user = user
				k=1
				break

		if k == 0:
			raise forms.ValidationError("Selectați un utilizator valid!")

		if not vehicle_driver.isalnum():
			raise forms.ValidationError("Doar caractere și cifre!")

		return my_user

	def clean_vehicle_category(self, *args, **kwargs):
		vehicle_category = self.cleaned_data.get('vehicle_category')
		category_list = Category.objects.all()
		k=0

		if not vehicle_category:
			return Category.objects.get(category_name='NONE')

		for cat in category_list:
			if cat.category_name.lower() == vehicle_category.lower():
				my_cat = cat
				k=1
				break

		if k == 0:
			raise forms.ValidationError("Selectați o categorie validă!")

		if not vehicle_category.isalnum():
			raise forms.ValidationError("Doar caractere și cifre!")

		return my_cat



class CategoryForm(forms.ModelForm):
	category_name = forms.CharField(label='Numele categoriei')
	class Meta:
		model = Category
		fields = [
			'category_name'
		]
	def clean_category_name(self, *args, **kwargs):
		category_name = self.cleaned_data.get('category_name')
		obj_list = Category.objects.all()
		for obj in obj_list:
			if category_name.lower() == obj.category_name.lower():
				raise forms.ValidationError("Această categorie este deja in baza de date!")

		if len(category_name) > 50:
			raise forms.ValidationError("Numele este prea lung (maxim 50 de caractere)!")

		if not category_name.isalpha():
			raise forms.ValidationError("Numele categoriei poate conține doar litere")
		return category_name.lower().capitalize()