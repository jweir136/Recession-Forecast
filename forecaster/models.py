from django.db import models

# Create your models here.
class Updates(models.Model):
	#hold the last day that the system updated itself.
	last_update = models.CharField(max_length=2)
	delta_yield = models.CharField(max_length=10)
	delta_vix = models.CharField(max_length=10)