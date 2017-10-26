from django.shortcuts import render
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView)
from .models import Project
# Create your views here.
class ProjectCreateView(CreateView):
    model = Project
    fields = '__all__'

class ProjectListView(ListView):
    model = Project
    fields = '__all__'

class ProjectDeleteView(DetailView):
    model = Project
