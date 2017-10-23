from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)

class ClientContact(models.Model):
    contact_person = models.OneToOneField(User)
