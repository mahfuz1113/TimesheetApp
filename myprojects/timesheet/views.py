from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.models import User
from django.db.models import Sum
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView
                                  )
from django.views.generic.edit import UpdateView
from .models import *
from .forms import *

from datetime import datetime, timedelta
from .helper_functions import dategenerator

# Create your views here.
class TimesheetCreateView(CreateView):
    model = TimesheetDetail
    fields = ['workdate', 'workcode', 'project', 'hours']

class TimesheetUpdateView(UpdateView):
    model = Timesheet
    fields = '__all__'

class TimesheetDetailListView(ListView):
    model = TimesheetDetail
    queryset = TimesheetDetail.objects.order_by('timesheet__employee','timesheet__weekenddate','workdate')

    def get_template_names(self, **kwargs):
        template_name = super(TimesheetDetailListView, self).get_template_names(**kwargs)
        if self.request.is_ajax():
            template_name = 'timesheet/_ajax_timesheetdetail_list.html'
        else:
            template_name = 'timesheet/timesheetdetail_list.html'

        return template_name

class TimesheetDetailView(DetailView):
    model = TimesheetDetail

class TimesheetDeleteView(DeleteView):
    model = TimesheetDetail

class TimesheetListView(ListView):
    model = Timesheet
    # queryset = Timesheet.objects.filter(weekenddate__weekenddate=self.kwargs['weekenddate']).order_by('employee','weekenddate')

    def get_context_data(self, **kwargs):
        context = super(TimesheetListView, self).get_context_data(**kwargs)
        timesheetdetails_list = TimesheetDetail.objects.filter(timesheet__weekenddate__weekenddate=self.kwargs['weekenddate']).select_related('timesheet').select_related('timesheet__employee').select_related('workcode').select_related('project').annotate(Sum('hours')).order_by('timesheet', 'workdate')

        context['timesheetdetails_list'] = timesheetdetails_list
        context['totalhoursbytimesheet'] = timesheetdetails_list.values('timesheet').annotate(Sum('hours')).order_by()
        context['totalhoursbytimesheetbyworkcode'] = timesheetdetails_list.values('timesheet','workcode__workcode').annotate(Sum('hours')).order_by('timesheet','workcode__workcode')
        context['workcode_no'] = Workcode.objects.all().order_by('workcode_serial')


        return context

    def get_queryset(self):
        return Timesheet.objects.filter(weekenddate__weekenddate=self.kwargs['weekenddate'])\
                                .select_related('employee')\
                                .select_related('weekenddate')\
                                .order_by('employee__name','weekenddate')

class WeekendDateListView(ListView):
    model = WeekendDate
    queryset = WeekendDate.objects.order_by('weekenddate')


def timesheet_data_entry_view(request):

    if request.method == "POST":
        timesheet_form = TimesheetForm(request.POST)

        if timesheet_form.is_valid():
            created_timesheet = timesheet_form.save(commit=False)
            formset = TimesheetFormSet(request.POST, request.FILES,
                                        instance=created_timesheet)

            if formset.is_valid():
                created_timesheet.save()
                formset.save()

            return HttpResponseRedirect(reverse('timesheet:timesheetlist'))
        else:
            return render(request, 'timesheet/timesheet_dataentry.html',
                            {'formset':formset})
    else:
        form = TimesheetForm()
        formset = TimesheetFormSet()

        return render(request, 'timesheet/timesheet_dataentry.html',
                        {'form':form, 'formset':formset})

def timesheet_formset(request, pk):
    timesheet = Timesheet.objects.get(pk=pk)
    TimesheetInlineFormset = forms.inlineformset_factory(
                                                Timesheet,
                                                TimesheetDetail,
                                                fields=('timesheet',
                                                        'workdate',
                                                        'workcode',
                                                        'project',
                                                        'hours'),
                                                        extra=0)
    # formset = TimesheetFormset()

    if request.method == "POST":
        formset = TimesheetInlineFormset(request.POST,request.FILES,
                                            instance=timesheet)

        if formset.is_valid():
            formset.save(commit=True)
            return HttpResponseRedirect(reverse('timesheet:timesheetlist'))

        # else:
            # formset = TimesheetInlineFormSet(instance=author)
            # return render(request, 'timesheet/timesheet_dataentry_formset.html',{'formset':formset})
    else:
        formset = TimesheetInlineFormset(instance=timesheet)
    return render(request, 'timesheet/timesheet_dataentry_formset.html',
                                    {'formset':formset})

#####################
#####################


def test_formset_initial_data(request, pk, weekenddate):
    timesheet_instance = Timesheet.objects.get(employee__pk=pk, weekenddate__weekenddate=weekenddate)

    # initial_data = dategenerator(weekenddate)
    # print(initial_data)
    # initial_data = [{'workcode': 3, 'project':2, 'workdate': '2017-01-02', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-03', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-04', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-05', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-06', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-07', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6},
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-08', 'hours':0, 'workcode1':3 , 'workcode2':4 , 'workcode3':5,  'workcode4':6}]

    if request.method == "POST":
        form = TimesheetForm(request.POST)
        # created_timesheet = form.save(commit=False)
        # newtimesheet_id = created_timesheet.id
        # newtimesheet = created_timesheet
        # formset = TimesheetFormSet(request.POST, request.FILES,
        #                             instance=created_timesheet)
        if form.is_valid():
            created_timesheet = form.save(commit=False)
            newtimesheet_id = created_timesheet.id
            newtimesheet = created_timesheet
            formset = TimesheetFormSet(request.POST, request.FILES,
                                        instance=created_timesheet)
            print('form valid! Check formset')
            if formset.is_valid():
                print('Form and Formset valid')
                created_timesheet.save()
                # formset.save()
            for form in formset:
                print('in formset loop')
                obj = form.save(commit=False)
                obj.timesheet = newtimesheet
                obj.workcode = Workcode.objects.get(id=5)
                # obj.project = Project.objects.get(id=3)
                if form.cleaned_data['workcode1'] is not None:
                    obj.workcode = Workcode.objects.get(id=1)
                    obj.hours = form.cleaned_data['workcode1']
                elif form.cleaned_data['workcode2'] is not None:
                    obj.workcode = Workcode.objects.get(id=4)
                    obj.hours = form.cleaned_data['workcode2']
                elif form.cleaned_data['workcode3'] is not None:
                    obj.workcode = Workcode.objects.get(id=5)
                    obj.hours = form.cleaned_data['workcode3']
                elif form.cleaned_data['workcode4'] is not None:
                    obj.workcode = Workcode.objects.get(id=6)
                    obj.hours = form.cleaned_data['workcode4']
                print('Line before save')
                # obj.save()
            formset.save()
            return HttpResponseRedirect(reverse('timesheet:timesheetlist'))
        else:
            return render(request, 'timesheet/timesheet_dataentry_test.html',
                            {'form': form, 'formset':formset})

    else:
        form = TimesheetForm()
        formset = TimesheetFormSet()

    return render(request, 'timesheet/timesheet_dataentry_test.html',
                    {'form': form, 'formset':formset})


def timesheet_with_extra_field(request):
    if request.method == 'POST':
        form = TimesheetDetailPreForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            print('workcode is:{}'.format(form.cleaned_data['workcode1']))
            print('hours is:{}'.format(form.cleaned_data['hours']))
    else:
        form = TimesheetDetailPreForm()

    return render(request, 'timesheet/timesheet_extra_field.html',
                        {'form': form})



def timesheet_data_entry_view_test(request):
    """ Timesheet view in a grid form. Referenced TimesheetForm has extra field for each workcode """
    # timesheet_instance = Timesheet.objects.get(pk=60)
    timesheet_instance = get_object_or_404(Timesheet, pk=60)
    # initial_data1 = [{'employee':1, 'weekenddate':1}]
    # initial_data = [{'workcode': 3, 'project':2, 'workdate': '2017-01-02', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-03', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-04', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-05', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-06', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-07', 'hours':0, },
    #                 {'workcode': 3, 'project':2, 'workdate': '2017-01-08', 'hours':0, }]
    initial_data = [{'workcode': 3, 'project':2, 'workdate': '2017-01-02', 'hours':0, 'workcode1':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-03', 'hours':0, 'workcode1':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-04', 'hours':0, 'workcode1':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-05', 'hours':0, 'workcode2':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-06', 'hours':0, 'workcode2':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-07', 'hours':0, 'workcode2':3 },
                    {'workcode': 3, 'project':2, 'workdate': '2017-01-08', 'hours':0, 'workcode2':3 }]


    if request.method == "POST":
        timesheet_form = TimesheetForm(request.POST)

        if timesheet_form.is_valid():
            emp=timesheet_form.cleaned_data['employee']
            we=timesheet_form.cleaned_data['weekenddate']
            print(emp)
            print(we)
            obj = Timesheet.objects.get(employee=emp,weekenddate=we)
            print(obj)
            # created_timesheet = timesheet_form.save(commit=False)
            # newtimesheet_id = created_timesheet.id
            newtimesheet_id = obj.id

            newtimesheet = created_timesheet
            formset = TimesheetFormSet(request.POST, request.FILES,
                                        instance=created_timesheet,
                                        initial=initial_data)

            if formset.is_valid():
                print('formset valid')
                # created_timesheet.save()
                # formset.save()
                for form in formset:
                    print('in formset loop')
                    obj = form.save(commit=False)
                    obj.timesheet = newtimesheet
                    obj.workcode = Workcode.objects.get(id=5)
                    # obj.project = Project.objects.get(id=3)
                    if form.cleaned_data['workcode1'] is not None:
                        obj.workcode = Workcode.objects.get(id=1)
                        obj.hours = form.cleaned_data['workcode1']
                    elif form.cleaned_data['workcode2'] is not None:
                        obj.workcode = Workcode.objects.get(id=4)
                        obj.hours = form.cleaned_data['workcode2']
                    elif form.cleaned_data['workcode3'] is not None:
                        obj.workcode = Workcode.objects.get(id=5)
                        obj.hours = form.cleaned_data['workcode3']
                    elif form.cleaned_data['workcode4'] is not None:
                        obj.workcode = Workcode.objects.get(id=6)
                        obj.hours = form.cleaned_data['workcode4']
                    print('Line before save')
                    # obj.save()
                formset.save()
                return HttpResponseRedirect(reverse('timesheet:timesheetlist'))
            else:
                print('formset not valid')
                print(formset.errors)
                return render(request, 'timesheet/timesheet_dataentry_test.html',
                                    {'form':form, 'formset':formset})
        else:
            print(timesheet_form.errors)
            return HttpResponse('error')
    else:
        form = TimesheetForm()
        formset = TimesheetFormSet(initial=initial_data)

        return render(request, 'timesheet/timesheet_dataentry_test.html',
                            {'form':form, 'formset':formset})


def manage_timesheet(request, user_id):
    """Edit children and their addresses for a single parent."""
    # pass
    initial_data = [{'workcode': 1, 'project':1, 'workdate': '2017-12-29', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-12-30', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-12-31', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-01', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-02', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-03', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-04', 'hours':0, }]
    parent = get_object_or_404(Employee, id=user_id)
    # parent = Employee.objects.all()

    if request.method == 'POST':
        formset = TimesheetFormSetNew(request.POST, instance=parent)
        if formset.is_valid():
            formset.save()
            # return HttpResponseRedirect(reverse('nestedformset:nestedformset', 'parent_id'= parent_id))
            return redirect('timesheet:timesheetlist')
    else:
        formset = TimesheetFormSetNew(instance=parent)

    return render(request, 'timesheet/manage_timesheet.html', {
                  'parent':parent,
                  'children_formset':formset})

#####################################################################
#####################################################################

def manage_timesheet1(request, timesheet_id):
    """Edit children and their addresses for a single parent."""

    initial_data = [{'workcode': 1, 'project':1, 'workdate': '2017-12-29', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-12-30', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-12-31', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-01', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-02', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-03', 'hours':0, },
                    {'workcode': 1, 'project':1, 'workdate': '2017-01-04', 'hours':0, }]
    timesheet = Timesheet.objects.get(pk=timesheet_id)
    if request.method == 'POST':
        formset = TimesheetDetailInlineFormset(request.POST, request.FILES, instance=timesheet, initial=initial_data)
        if formset.is_valid():
            print()
            print()

            print()

            print('***************************************************************************************************************************')
            print('***************************************************************************************************************************')
            print('***************************************************************************************************************************')

            for form in formset:
                print('*************************** in formset loop *****************************************************')
                obj = form.save(commit=False)
                obj.timesheet = timesheet
                obj.workcode = Workcode.objects.get(id=5)
                print('**** Starting Clean_data Loop ***********************************************************************************************************************')

                for k,v in form.cleaned_data.items():
                    print(k,v)
                # obj.project = Project.objects.get(id=3)
                if form.cleaned_data['normal'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=10)
                    obj.hours = form.cleaned_data['normal']
                    print(obj.hours)
                elif form.cleaned_data['rnr'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=80)
                    obj.hours = form.cleaned_data['rnr']
                    print(obj.hours)
                elif form.cleaned_data['annual_leave'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=20)
                    obj.hours = form.cleaned_data['annual_leave']
                    print(obj.hours)
                elif form.cleaned_data['personal_leave'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=21)
                    obj.hours = form.cleaned_data['personal_leave']
                    print(obj.hours)
                elif form.cleaned_data['carers_leave'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=25)
                    obj.hours = form.cleaned_data['carers_leave']
                    print(obj.hours)
                elif form.cleaned_data['long_service_leave'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=26)
                    obj.hours = form.cleaned_data['long_service_leave']
                    print(obj.hours)
                elif form.cleaned_data['night_shift'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=13)
                    obj.hours = form.cleaned_data['night_shift']
                    print(obj.hours)
                elif form.cleaned_data['afternoon_shift'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=14)
                    obj.hours = form.cleaned_data['afternoon_shift']
                    print(obj.hours)
                elif form.cleaned_data['bus_driving'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=71)
                    obj.hours = form.cleaned_data['bus_driving']
                    print(obj.hours)
                elif form.cleaned_data['work_comp'] is not None:
                    obj.workcode = Workcode.objects.get(workcode=22)
                    obj.hours = form.cleaned_data['work_comp']
                    print(obj.hours)

            # formset.save()
            # return HttpResponseRedirect(reverse('nestedformset:nestedformset', 'parent_id'= parent_id))
            return redirect('timesheet:timesheetlist')
        else:
            print(formset.errors)
    else:
        formset = TimesheetDetailInlineFormset(instance=timesheet, initial=initial_data)

    if request.is_ajax():
        return render(request, 'timesheet/_ajax_manage_timesheet.html', {
                      'children_formset':formset, 'timesheetid':timesheet_id})
    else:
        return render(request, 'timesheet/manage_timesheet.html', {
                      'children_formset':formset, 'timesheetid':timesheet_id})
