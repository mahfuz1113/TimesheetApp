from django.db import models
from django.contrib.auth.models import User
from project.models import Project
from item.models import Item
from client.models import Client, ClientContact

# Create your models here.
class QuoteStatus(models.Model):
    description = models.CharField(max_length=40)
    code = models.SmallIntegerField()

class Quotation(models.Model):
    project = models.ForeignKey(Project)
    client = models.ForeignKey(Client)
    requestor = models.ForeignKey(ClientContact)
    preparer = models.ForeignKey(User)
    status = models.ForeignKey(QuoteStatus)
    version = models.SmallIntegerField()
    description = models.CharField(max_length = 200)
    quotation_date = models.DateField()
    work_order = models.CharField(max_length=15)
    as_sold = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)


    unique_together = ['project', 'version']

class QuotationLineItem(models.Model):
    quote = models.ForeignKey(Quotation)
    item = models.ForeignKey(Item)
    description = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseOrderStatus(models.Model):
    description = models.CharField(max_length=40)
    code = models.SmallIntegerField()

class PurchaseOrder(models.Model):
    client = models.ForeignKey(Client)
    status = models.ForeignKey(PurchaseOrderStatus)
    quotation = models.ForeignKey(Quotation)
    purcahse_order_date = models.DateField()
    purchase_order_number = models.CharField(max_length=15)
    description = models.CharField(max_length = 200)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)

    unique_together = ['purchase_order_number',]

class PurchaseOrderLineItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    line = models.SmallIntegerField()
    description = models.CharField(max_length=50)
    when = models.DateField()
    where = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
