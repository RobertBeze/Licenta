from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from pages.models import DetaliiFoaieParcurs


class UserForm(forms.Form):
	username = forms.CharField(label="Nume", min_length=4, max_length=150)
	password1 = forms.CharField(label="Parola", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Repetă parola", widget=forms.PasswordInput)
	admin = forms.BooleanField(label="Administrator", required = False)

	username.widget.attrs.update({'class':'form-control w-25'})
	password1.widget.attrs.update({'class':'form-control w-25'})
	password2.widget.attrs.update({'class':'form-control w-25'})
	admin.widget.attrs.update({'class':'form-radio'})


	def clean_username(self):
		username = self.cleaned_data.get('username')
		r = User.objects.filter(username=username)
		if r.count():
			raise forms.ValidationError("Acest nume de utilizator deja există!")
		return username

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Parolele diferă!")

		return password2

	def save(self, commit = True):
		if not self.cleaned_data['admin']:
			user = User.objects.create_user(username = self.cleaned_data['username'], email=None, password = self.cleaned_data['password1'])
		else:
			user = User.objects.create_superuser(username = self.cleaned_data['username'], email=None, password = self.cleaned_data['password1'])
		return user

class UserPwd(forms.Form):
	password1 = forms.CharField(label="Parola nouă", widget=forms.PasswordInput)
	password2 = forms.CharField(label="Repetă parola", widget=forms.PasswordInput)


	password1.widget.attrs.update({'class':'form-control w-25'})
	password2.widget.attrs.update({'class':'form-control w-25'})


	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Parolele diferă!")

		return password2



class TimePickerInput(forms.TimeInput):
	input_type = 'time'


class DetaliuFoaieForm(forms.Form):
	departure = forms.CharField(label='Loc. Plecare')
	arrival = forms.CharField(label='Loc. Destinatie')
	date_departure = forms.TimeField(label="Ora Plecare", widget=TimePickerInput)
	date_arrival = forms.TimeField(label="Ora sosire", widget=TimePickerInput)
	km =  forms.IntegerField(label="KM Parcursi")

	departure.widget.attrs.update({'class':'form-control w-25'})
	arrival.widget.attrs.update({'class':'form-control w-25'})
	date_departure.widget.attrs.update({'class':'form-control w-25'})
	date_arrival.widget.attrs.update({'class':'form-control w-25'})
	km.widget.attrs.update({'class':'form-control w-25'})

	def clean_departure(self):
		departure = self.cleaned_data.get('departure')
		if len(departure)>100:
			raise forms.ValidationError('Maxim 100 de caractere')

		res = bool(re.match('[a-zA-Z\s\.\-]+$',departure))
		if not res:
			raise forms.ValidationError('Doar litere, puncte si spatii sunt permise')
		return departure

	def clean_arrival(self):
		arrival = self.cleaned_data.get('arrival')
		if len(arrival)>100:
			raise forms.ValidationError('Maxim 100 de caractere')
		res = bool(re.match('[a-zA-Z\s\.\-]+$',arrival))
		if not res:
			raise forms.ValidationError('Doar litere, puncte si spatii sunt permise')
		return arrival

	def clean_km(self):
		km = self.cleaned_data.get('km')
		if km <0:
			raise forms.ValidationError('Doar numere intregi')
		return km

class DetaliuUpdateForm(forms.ModelForm):
	departure = forms.CharField(label='Loc. Plecare')
	arrival = forms.CharField(label='Loc. Destinatie')
	date_departure = forms.TimeField(label="Ora Plecare", widget=TimePickerInput)
	date_arrival = forms.TimeField(label="Ora sosire", widget=TimePickerInput)
	km =  forms.IntegerField(label="KM Parcursi")

	departure.widget.attrs.update({'class':'form-control w-25'})
	arrival.widget.attrs.update({'class':'form-control w-25'})
	date_departure.widget.attrs.update({'class':'form-control w-25'})
	date_arrival.widget.attrs.update({'class':'form-control w-25'})
	km.widget.attrs.update({'class':'form-control w-25'})

	class Meta:
		model = DetaliiFoaieParcurs
		fields = [
			'departure',
			'arrival',
			'date_departure',
			'date_arrival',
			'km',
		]

	def clean_km(self):
		km = self.cleaned_data.get('km')
		if km <0:
			raise forms.ValidationError('Doar numere intregi')
		return km

	def clean_departure(self):
		departure = self.cleaned_data.get('departure')
		if len(departure)>100:
			raise forms.ValidationError('Maxim 100 de caractere')

		res = bool(re.match('[a-zA-Z\s\.\-]+$',departure))
		if not res:
			raise forms.ValidationError('Doar litere, puncte si spatii sunt permise')
		return departure

	def clean_arrival(self):
		arrival = self.cleaned_data.get('arrival')
		if len(arrival)>100:
			raise forms.ValidationError('Maxim 100 de caractere')
		res = bool(re.match('[a-zA-Z\s\.\-]+$',arrival))
		if not res:
			raise forms.ValidationError('Doar litere, puncte si spatii sunt permise')
		return arrival