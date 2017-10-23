from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Invoice)
admin.site.register(InvoiceStatus)
admin.site.register(PaymentTerm)
admin.site.register(InvoiceLineItem)
