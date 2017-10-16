from django.db import models

# Create your models here.
class Parent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Child(models.Model):
    parent = models.ForeignKey(Parent)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Address(models.Model):
    child = models.ForeignKey(Child)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
