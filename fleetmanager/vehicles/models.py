from django.db import models
from django.conf import settings
from django.urls import reverse





# Create your models here.

class Category(models.Model):
	category_name = models.CharField(max_length = 50, unique = True, verbose_name = "Categorie")

	def get_name(self):
		return self.category_name

	def __str__(self):
		return self.category_name

class Vehicle(models.Model):
	vehicle_plate = models.CharField(max_length = 10, unique = True, verbose_name = "Număr înmatriculare")
	vehicle_odometer = models.PositiveIntegerField(verbose_name = "Kilometraj")
	vehicle_itp = models.DateField(verbose_name = "ITP expiră la")
	vehicle_rca = models.DateField(verbose_name = "RCA expiră la")
	vehicle_last_service = models.PositiveIntegerField(verbose_name = "Ultimul service efectuat KM")
	vehicle_driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True, verbose_name = "Șoferul", blank = True)
	vehicle_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null = True, verbose_name = "Categoria", blank = True)

	def __str__(self):
		if self.vehicle_category is None:
			string = "Număr: "+self.vehicle_plate+" | Categorie: None"
		else:
			string = "Număr: "+self.vehicle_plate+" | Categorie: "+self.vehicle_category.get_name()

		return string

	def get_absolute_url(self):
		return reverse("vehicle-detail-view", kwargs={"id":self.id})

