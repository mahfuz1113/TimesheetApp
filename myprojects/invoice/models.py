from django.db import models
from quotation.models import PurchaseOrder
from project.models import Project
from item.models import Item
# Create your models here.
class InvoiceStatus(models.Model):
    description = models.CharField(max_length=40)
    code = models.SmallIntegerField()

class PaymentTerm(models.Model):
    description = models.CharField(max_length=20)
    code = models.SmallIntegerField()

class Invoice(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    project = models.ForeignKey(Project)
    status = models.ForeignKey(InvoiceStatus)
    invoice_number = models.CharField(max_length=15)
    description = models.CharField(max_length=50)

    invoice_date = models.DateField()
    submition_date = models.DateField()
    due_date = models.DateField()
    payment_date = models.DateField()

    payment_term = models.ForeignKey(PaymentTerm)

    total_ex_gst = models.DecimalField(max_digits=10, decimal_places=2)
    gst = models.DecimalField(max_digits=10, decimal_places=2)
    total_incl_gst = models.DecimalField(max_digits=10, decimal_places=2)

class InvoiceLineItem(models.Model):

    invoice = models.ForeignKey(Invoice)
    item = models.ForeignKey(Item)
    description = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
