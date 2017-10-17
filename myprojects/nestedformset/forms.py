from django.forms.models import inlineformset_factory, BaseInlineFormSet

from . import models




class BaseChildrenFormset(BaseInlineFormSet):
    # pass
    def add_fields(self, form, index):
        super(BaseChildrenFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = AddressFormset(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='address-%s-%s' % (
                            form.prefix,
                            AddressFormset.get_default_prefix()),
                        )

    def is_valid(self):
        result = super(BaseChildrenFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseChildrenFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


ChildrenFormset = inlineformset_factory(models.Parent, models.Child, formset=BaseChildrenFormset, fields="__all__", extra=1)
AddressFormset = inlineformset_factory(models.Child, models.Address, fields="__all__", extra=1)
