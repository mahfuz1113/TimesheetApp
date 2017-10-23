from django.db import models

# Create your models here.
class Item(models.Model):
    code = models.CharField(max_length=8)
    description = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    ismaterial = models.BooleanField()
    islabour = models.BooleanField()
