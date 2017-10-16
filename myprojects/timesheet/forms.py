from django import forms
from . import models
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet, modelformset_factory, BaseModelFormSet
from django.contrib.auth.models import User


class TimesheetForm(forms.ModelForm):
    class Meta:
        model = models.Timesheet
        fields = "__all__"

class TimesheetDetailPreForm(forms.ModelForm):
    workcode1 = forms.IntegerField(max_value=16, min_value=0, label='Norm', required=False)
    workcode2 = forms.IntegerField(max_value=16, min_value=0, label='R&R', required=False)
    workcode3 = forms.IntegerField(max_value=16, min_value=0, label='AL', required=False)
    workcode4 = forms.IntegerField(max_value=16, min_value=0, label='SL', required=False)

    class Meta:
        model = models.TimesheetDetail
        # fields = '__all__'
        fields = ['workdate', 'project', 'hours', 'workcode1', 'workcode2', 'workcode3', 'workcode4', 'workcode',]

    # def clean_hours(self):
    #     data = 30 #self.data.get('hours')
    #     print('workcode1 {}'.format(self.cleaned_data.get('workcode1')))
    #     print(('hours is: {}').format(self.cleaned_data['hours']))
    #     return data


# TimesheetDetailPreForm has extra field added for data collection
TimesheetFormSet = forms.inlineformset_factory(models.Timesheet,
                                                models.TimesheetDetail,
                                                form=TimesheetDetailPreForm,
                                                extra=7, max_num=7)

class BaseTimesheetFormSet(forms.BaseFormSet):
    def add_fields(self, form, index):
        super(BaseTimesheetFormSet, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = TimesheetFormSet(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='address-%s-%s' % (
                            form.prefix,
                            TimesheetFormSet.get_default_prefix()),
                        )

    def is_valid(self):
        result = super(BaseTimesheetFormSet, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseTimesheetFormSet, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result



TimesheetDetailFormSet = forms.formset_factory(models.TimesheetDetail,
                                            formset=BaseTimesheetFormSet
                                            )



############################################################################################
############################################################################################
############################################################################################


class BaseTimesheetFormsetNew(BaseInlineFormSet):
    # pass
    def add_fields(self, form, index):
        super(BaseTimesheetFormsetNew, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = TimesheerDetailFormsetNew(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='address-%s-%s' % (
                            form.prefix,
                            TimesheerDetailFormsetNew.get_default_prefix()),
                        )

    def is_valid(self):
        result = super(BaseTimesheetFormsetNew, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseTimesheetFormsetNew, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

TimesheetFormSetNew = inlineformset_factory(models.Employee, models.Timesheet, formset=BaseTimesheetFormsetNew, fields="__all__", extra=1)
TimesheerDetailFormsetNew = inlineformset_factory(models.Timesheet, models.TimesheetDetail, fields="__all__", extra=1)

###############################################################
###############################################################

class BaseTimesheetFormsetNew1(BaseModelFormSet):



    def add_fields(self, form, index):
        super(BaseTimesheetFormsetNew1, self).add_fields(form, index)
        # form.fields['workcode1'] = forms.IntegerField(max_value=16, min_value=0, label='Norm', required=False)
        # form.fields['workcode2'] = forms.IntegerField(max_value=16, min_value=0, label='R&R', required=False)
        # form.fields['workcode3'] = forms.IntegerField(max_value=16, min_value=0, label='AL', required=False)
        # form.fields['workcode4'] = forms.IntegerField(max_value=16, min_value=0, label='SL', required=False)
        # save the formset in the 'nested' property
        form.nested = TimesheetDetailFormsetNew1(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='address-%s-%s' % (
                            form.prefix,
                            TimesheetDetailFormsetNew1.get_default_prefix()),
                        )

    def is_valid(self):
        result = super(BaseTimesheetFormsetNew1, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseTimesheetFormsetNew1, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


class BaseTimesheetInlineFormSet(BaseInlineFormSet):

        def add_fields(self, form, index):
            super(BaseTimesheetInlineFormSet, self).add_fields(form, index)
            form.fields['10']               = forms.IntegerField(max_value=16, min_value=0, label='Norm', required=False)
            form.fields['80']                  = forms.IntegerField(max_value=16, min_value=0, label='RnR', required=False)
            form.fields['20']         = forms.IntegerField(max_value=16, min_value=0, label='Annu', required=False)
            form.fields['21']       = forms.IntegerField(max_value=16, min_value=0, label='Sick', required=False)
            form.fields['25']         = forms.IntegerField(max_value=16, min_value=0, label="Carer", required=False)
            form.fields['26']   = forms.IntegerField(max_value=16, min_value=0, label='LSL', required=False)
            form.fields['13']          = forms.IntegerField(max_value=16, min_value=0, label='Night', required=False)
            form.fields['14']      = forms.IntegerField(max_value=16, min_value=0, label="Noon", required=False)
            form.fields['71']          = forms.IntegerField(max_value=16, min_value=0, label='Bus', required=False)
            form.fields['22']            = forms.IntegerField(max_value=16, min_value=0, label='WComp', required=False)

TimesheetFormSetNew1 = modelformset_factory(models.Timesheet,
                                            form=TimesheetForm,
                                            formset=BaseTimesheetFormsetNew1,
                                            fields="__all__", extra=1)
TimesheetDetailFormsetNew1 = inlineformset_factory(models.Timesheet,
                                                    models.TimesheetDetail,
                                                    form = TimesheetForm,
                                                    formset=BaseTimesheetInlineFormSet,
                                                    fields="__all__",
                                                    extra=7, max_num=7)
TimesheetDetailInlineFormset = inlineformset_factory(models.Timesheet,
                                                    models.TimesheetDetail,
                                                    form = TimesheetForm,
                                                    formset=BaseTimesheetInlineFormSet,
                                                    # fields=('workdate','project'),
                                                    fields='__all__',
                                                    extra=7, max_num=9)
