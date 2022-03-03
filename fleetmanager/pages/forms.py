from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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