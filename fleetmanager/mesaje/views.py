from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Message
from django.contrib.auth.models import User
from itertools import chain
# Create your views here.


class InboxView(View):
	template_name = 'mesaje/inbox.html'

	def get(self, request, *args, **kwargs):
		mesaje = Message.objects.filter(user=request.user)
		lista = []
		for mesaj in mesaje:
			if mesaj.sender != request.user:
				lista.append(mesaj.sender.username)

		context={'utilizatori' : lista}
		return render(request, self.template_name, context)


class InboxWithView(View):
	template_name = 'mesaje/mesaje.html'

	def get(self, request, username, *args, **kwargs):
		lista = User.objects.filter(username=username)
		if lista.count() != 0:
			usr = lista[0]
		else:
			return redirect('inbox')
		mesaje_primite = Message.objects.filter(user=request.user, sender=usr)
		mesaje_trimise = Message.objects.filter(user=request.user, sender=request.user, recipient=usr)
		mesaje = list(chain(mesaje_trimise, mesaje_primite))
		mesaje.sort(key=lambda x: x.date, reverse=False)

		for mesaj in mesaje:
			print(mesaj.body)

		context = {'recipient' : username, 'mesaje':mesaje}
		return render(request, self.template_name, context)