from django import forms
from .models import *
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet, modelformset_factory, BaseModelFormSet
from django.contrib.auth.models import User

class CarBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(CarBaseInlineFormSet, self).add_fields(form, index)
        form.fields['workcode1'] = forms.IntegerField(max_value=16, min_value=0, label='Norm', required=False)
        form.fields['workcode2'] = forms.IntegerField(max_value=16, min_value=0, label='R&R', required=False)
        form.fields['workcode3'] = forms.IntegerField(max_value=16, min_value=0, label='AL', required=False)
        form.fields['workcode4'] = forms.IntegerField(max_value=16, min_value=0, label='SL', required=False)


CarInlineFormSet = inlineformset_factory(Owner,Car, formset=CarBaseInlineFormSet, fields='__all__',extra=1)
# CarInlineFormSet = inlineformset_factory(Owner,Car, fields='__all__',extra=1)
