from django.shortcuts import render, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import *
from .forms import *
from .mixin import *
from django.urls import reverse_lazy

from django.http import JsonResponse
# from django.views.generic.edit import CreateView
# from myapp.models import Author


# Create your views here.


class CarListView(ListView):
        model = Car
        fields = '__all__'

        def get_template_names(self, **kwargs):
            template_name = super(CarListView, self).get_template_names(**kwargs)
            if self.request.is_ajax():
                template_name = 'modalform/car_ajax_list.html'
            else:
                template_name = 'modalform/car_list.html'

            return template_name


class CarCreateView(CreateView):
        model = Car
        fields='__all__'
        success_url = reverse_lazy('modalform:carlistview')


class CarUpdateView(UpdateView):
    model = Car
    fields = '__all__'
    success_url = reverse_lazy('modalform:carlistview')
    template_name_suffix = '_update_form'

class CarDeleteView(DeleteView):
    model = Car
    success_url = reverse_lazy('modalform:carlistview')

def CarInlineFormSetView(request, owner_id):
    owner = Owner.objects.get(pk=owner_id)
    if request.method == "POST":
        formset = CarInlineFormSet(request.POST,request.FILES, instance=owner)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data.get('workcode1'))
                print(form.cleaned_data.get('workcode2'))
                print(form.cleaned_data.get('workcode3'))
                print(form.cleaned_data.get('workcode4'))
            formset.save()
            return HttpResponse('Done')
    else:
        formset = CarInlineFormSet(instance=owner)

    return render(request, 'modalform/manage_cars.html', {'formset':formset})
