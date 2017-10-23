from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Quotation)
admin.site.register(QuotationLineItem)
admin.site.register(QuoteStatus)
admin.site.register(PurchaseOrderStatus)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLineItem)
