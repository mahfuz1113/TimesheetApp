from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
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
    print(request.method)
    timesheet_instance = get_object_or_404(Timesheet, pk=20)
    print()
    print()
    # print(timesheet_instance)
    print()
    print()
    print()

    # timesheet_detail_data = TimesheetDetail.objects.filter(timesheet=timesheet_instance).select_related('timesheet').select_related('timesheet__employee').select_related('workcode').select_related('project').annotate(Sum('hours')).order_by('timesheet', 'workdate')
    timesheet_detail_data = TimesheetDetail.objects.filter(timesheet=timesheet_instance).select_related('timesheet').prefetch_related('timesheet__employee').prefetch_related('workcode').prefetch_related('project').order_by('timesheet', 'workdate')


    print(timesheet_detail_data)
    print()
    print()
    print()
    initial_data = []
    # dict_key_list = ['workcode':,'project','workdate','workcode_10','workcode_80','workcode_20,','workcode_21','workcode_25','workcode_26','workcode_13','workcode_14','workcode_71','workcode_22']
    for ts in timesheet_detail_data:
        print('hello')

        for initd in initial_data:
            print('hi')
            print(ts)
            print(initd)
            print('********************')
            print('********************')
            print('********************')
            print('********************')

            if initd['project']==ts.project and initd['workdate'] == ts.workdate:
                print('match found')
                wc = 'workcode_'+str(ts.workcode.workcode)
                td_dict[wc] = ts.hours
                break
        else:
            td_dict = { 'workcode': None,'project':None,'workdate':None,
                        'workcode_10':None,'workcode_80':None,'workcode_20':None,
                        'workcode_21':None,'workcode_25':None,'workcode_26':None,
                        'workcode_13':None,'workcode_14':None,'workcode_71':None,
                        'workcode_22':None}
            wc = 'workcode_'+str(ts.workcode.workcode)
            td_dict[wc] = ts.hours
            td_dict['workdate'] = ts.workdate
            td_dict['project'] = ts.project
            td_dict['workcode'] = ts.workcode.workcode

            initial_data.append(td_dict)

    print(initial_data)

    if request.method == "POST":
        # timesheet_form = TimesheetForm(request.POST)
        # print(timesheet_form)
            formset = TimesheetFormSet(request.POST, request.FILES,
                                        instance=timesheet_instance,
                                        initial=initial_data)
        # print('************************************************************************************ timesheet form ************')
        # # print(timesheet_form)
        # print()
        # print('************************************************************************************ checking if timesheet form is valid ************')
        #
            if formset.is_valid():
                print('formset valid')
                # created_timesheet.save()
                # formset.save()
                for form in formset:
                    print('*************************** in formset loop doing something with a form *****************************************************')
                    print(form.changed_data)

                    if form.has_changed():
                        print()
                        print('form has changed')
                        # print(form.cleaned_data['workdate'])
                        print('******************** Starting Clean_data Loop *******************************************************************************************************')
                        wc_list = ['workcode_10','workcode_80','workcode_20','workcode_21','workcode_25','workcode_26','workcode_13','workcode_14','workcode_71','workcode_22']

                        for k,v in form.cleaned_data.items():
                            # print(('loop1 {} {}').format(k,v))

                            if k in wc_list and k in form.changed_data:
                                # print(('in both wc_list & changed_data <>{} - {}<>').format(k,v))
                                # print(k)
                                if v is not None:
                                    print(('V is not none {} {}').format(k,v))

                                    obj, created = TimesheetDetail.objects.update_or_create(
                                            # pk = form.cleaned_data['id'].id,
                                            timesheet = timesheet_instance,
                                            workcode = Workcode.objects.get(workcode=k[-2:]),
                                            project = form.cleaned_data['project'],
                                            workdate = form.cleaned_data['workdate'],
                                            defaults = {
                                                'timesheet' : timesheet_instance,
                                                'workcode' : Workcode.objects.get(workcode=k[-2:]),
                                                'project' : form.cleaned_data['project'],
                                                'workdate' : form.cleaned_data['workdate'],
                                                'hours' : v
                                                }
                                    )
                                    print(('{} {}').format(created, obj))
                                elif v is None:
                                    print(('V is none {} {}').format(k,v))
                                    obj = get_object_or_404(TimesheetDetail,
                                            timesheet = timesheet_instance,
                                            workcode = Workcode.objects.get(workcode=k[-2:]),
                                            project = form.cleaned_data['project'],
                                            workdate = form.cleaned_data['workdate'])
                                    obj.delete()
                # formset.save()

                return HttpResponseRedirect(reverse('timesheet:ts-dataentry'))

            else:
                print('formset not valid')
                print(formset.errors)
                return render(request, 'timesheet/timesheet_dataentry_test.html',
                                    {'form':form, 'formset':formset})
        # else:
        #     print(timesheet_form.errors)
        #     # return HttpResponse('error')
        #     return render(request, 'timesheet/timesheet_dataentry_test.html',
        #                         {'form':timesheet_form, 'formset':formset})
    else:

        # form = TimesheetForm(instance=timesheet_instance)
        formset = TimesheetFormSet(initial=initial_data)

        return render(request, 'timesheet/timesheet_dataentry_test.html',
                            {'formset':formset})


#####################################################################
#####################################################################
#####################################################################
#####################################################################
#####################################################################

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
#####################################################################
#####################################################################
#####################################################################


def manage_timesheet1(request, timesheet_id):

    print(request.method)
    timesheet_instance = get_object_or_404(Timesheet, pk=timesheet_id)
    print()
    print()
    # print(timesheet_instance)
    print()
    print()
    print()

    # timesheet_detail_data = TimesheetDetail.objects.filter(timesheet=timesheet_instance).select_related('timesheet').select_related('timesheet__employee').select_related('workcode').select_related('project').annotate(Sum('hours')).order_by('timesheet', 'workdate')
    timesheet_detail_data = TimesheetDetail.objects.filter(timesheet=timesheet_instance).select_related('timesheet').prefetch_related('timesheet__employee').prefetch_related('workcode').prefetch_related('project').order_by('timesheet', 'workdate')


    print(timesheet_detail_data)
    print()
    print()
    print()
    initial_data = []
    # dict_key_list = ['workcode':,'project','workdate','workcode_10','workcode_80','workcode_20,','workcode_21','workcode_25','workcode_26','workcode_13','workcode_14','workcode_71','workcode_22']
    for ts in timesheet_detail_data:
        print('hello')

        for initd in initial_data:
            print('hi')
            print(ts)
            print(initd)
            print('********************')
            print('********************')
            print('********************')
            print('********************')

            if initd['project']==ts.project and initd['workdate'] == ts.workdate:
                print('match found')
                wc = 'workcode_'+str(ts.workcode.workcode)
                td_dict[wc] = ts.hours
                break
        else:
            td_dict = { 'workcode': None,'project':None,'workdate':None,
                        'workcode_10':None,'workcode_80':None,'workcode_20':None,
                        'workcode_21':None,'workcode_25':None,'workcode_26':None,
                        'workcode_13':None,'workcode_14':None,'workcode_71':None,
                        'workcode_22':None}
            wc = 'workcode_'+str(ts.workcode.workcode)
            td_dict[wc] = ts.hours
            td_dict['workdate'] = ts.workdate
            td_dict['project'] = ts.project
            td_dict['workcode'] = ts.workcode.workcode

            initial_data.append(td_dict)

    print(initial_data)

    if request.method == "POST":
        # timesheet_form = TimesheetForm(request.POST)
        # print(timesheet_form)
            formset = TimesheetFormSet(request.POST, request.FILES,
                                        instance=timesheet_instance,
                                        initial=initial_data)
        # print('************************************************************************************ timesheet form ************')
        # # print(timesheet_form)
        # print()
        # print('************************************************************************************ checking if timesheet form is valid ************')
        #
            if formset.is_valid():
                print('formset valid')
                # created_timesheet.save()
                # formset.save()
                for form in formset:
                    print('*************************** in formset loop doing something with a form *****************************************************')
                    print(form.changed_data)

                    if form.has_changed():
                        print()
                        print('form has changed')
                        # print(form.cleaned_data['workdate'])
                        print('******************** Starting Clean_data Loop *******************************************************************************************************')
                        wc_list = ['workcode_10','workcode_80','workcode_20','workcode_21','workcode_25','workcode_26','workcode_13','workcode_14','workcode_71','workcode_22']

                        for k,v in form.cleaned_data.items():
                            # print(('loop1 {} {}').format(k,v))

                            if k in wc_list and k in form.changed_data:
                                # print(('in both wc_list & changed_data <>{} - {}<>').format(k,v))
                                # print(k)
                                if v is not None:
                                    print(('V is not none {} {}').format(k,v))

                                    obj, created = TimesheetDetail.objects.update_or_create(
                                            # pk = form.cleaned_data['id'].id,
                                            timesheet = timesheet_instance,
                                            workcode = Workcode.objects.get(workcode=k[-2:]),
                                            project = form.cleaned_data['project'],
                                            workdate = form.cleaned_data['workdate'],
                                            defaults = {
                                                'timesheet' : timesheet_instance,
                                                'workcode' : Workcode.objects.get(workcode=k[-2:]),
                                                'project' : form.cleaned_data['project'],
                                                'workdate' : form.cleaned_data['workdate'],
                                                'hours' : v
                                                }
                                    )
                                    print(('{} {}').format(created, obj))
                                elif v is None:
                                    print(('V is none {} {}').format(k,v))
                                    obj = get_object_or_404(TimesheetDetail,
                                            timesheet = timesheet_instance,
                                            workcode = Workcode.objects.get(workcode=k[-2:]),
                                            project = form.cleaned_data['project'],
                                            workdate = form.cleaned_data['workdate'])
                                    obj.delete()
                # formset.save()

                return HttpResponseRedirect(reverse('timesheet:ts-dataentry'))

            else:
                print('formset not valid')
                print(formset.errors)
                return render(request, 'timesheet/timesheet_dataentry_test.html',
                                    {'form':form, 'formset':formset})
        # else:
        #     print(timesheet_form.errors)
        #     # return HttpResponse('error')
        #     return render(request, 'timesheet/timesheet_dataentry_test.html',
        #                         {'form':timesheet_form, 'formset':formset})
    else:

        # form = TimesheetForm(instance=timesheet_instance)
        formset = TimesheetFormSet(initial=initial_data)


    if request.is_ajax():
        return render(request, 'timesheet/_ajax_manage_timesheet.html', {
                      'children_formset':formset, 'timesheetid':timesheet_id})
    else:
        return render(request, 'timesheet/manage_timesheet.html', {
                      'children_formset':formset, 'timesheetid':timesheet_id})
