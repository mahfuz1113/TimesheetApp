from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from . import models
from . import forms

# Create your views here.
def manage_children(request, parent_id):
    """Edit children and their addresses for a single parent."""
    # pass
    print(parent_id)
    parent = get_object_or_404(models.Parent, id=parent_id)

    if request.method == 'POST':
        formset = forms.ChildrenFormset(request.POST, instance=parent)
        if formset.is_valid():
            formset.save()
            # return HttpResponseRedirect(reverse('nestedformset:nestedformset', 'parent_id'= parent_id))
            return redirect('nestedformset:nestedformset', parent_id=parent.id)
    else:
        formset = forms.ChildrenFormset(instance=parent)

    return render(request, 'nestedformset/manage_children.html', {
                  'parent':parent,
                  'children_formset':formset})
