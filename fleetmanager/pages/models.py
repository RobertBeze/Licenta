from django.db import models
from django.conf import settings
from vehicles.models import Vehicle

# Create your models here.

class FoaieParcurs(models.Model):
	vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, verbose_name="Nr. Înmatriculare", blank = True)
	creation_date = models.DateField(verbose_name="Data")
	data_expirare = models.DateField(verbose_name="Data Expirare")
	expired = models.BooleanField(default=False)
	procesat = models.BooleanField(default=False)

class DetaliiFoaieParcurs(models.Model):
	foaie = models.ForeignKey(FoaieParcurs, on_delete=models.SET_NULL, null=True, verbose_name="ID Foaie Parcurs", blank = True)
	departure = models.CharField(max_length = 100, verbose_name = "Loc. Plecare")
	arrival = models.CharField(max_length = 100, verbose_name = "Loc. Destinatie")
	date_departure = models.TimeField(verbose_name="Ora plecare")
	date_arrival = models.TimeField(verbose_name="Ora sosire")
	km =  models.PositiveIntegerField(verbose_name = "Kilometri parcursi")