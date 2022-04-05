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
		lista_utilizatori = User.objects.exclude(id=request.user.id)
		lista = {}
		for mesaj in mesaje:
			if mesaj.recipient == request.user:
				if mesaj.sender.username in lista.keys():
					if lista[mesaj.sender.username] == True and mesaj.is_read == False:
						lista[mesaj.sender.username] = False
				else:
					lista[mesaj.sender.username] = mesaj.is_read
			elif mesaj.sender == request.user:
				lista[mesaj.recipient.username] = True

		context={'utilizatori' : lista, 'lista' : lista_utilizatori}
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
			mesaj.is_read = True
			mesaj.save()

		context = {'recipient' : username, 'mesaje':mesaje}
		return render(request, self.template_name, context)

	def post(self, request, username, *args, **kwargs):
		lista = User.objects.filter(username=username)
		if lista.count() != 0:
			usr = lista[0]
		else:
			return redirect('inbox')

		mesaj = request.POST['msgbody']
		Message.send_message(request.user, usr, mesaj);
		return redirect('direct-msg', username = username)