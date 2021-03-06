from django.db import models

# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Car(models.Model):
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    door = models.IntegerField()
    owner = models.ForeignKey(Owner)
    price = models.IntegerField()

    def __str__(self):
        return self.make + " " +self.model


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return self.headline
