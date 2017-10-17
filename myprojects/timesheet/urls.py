from django.conf.urls import url
from .views import *

app_name = 'timesheet'

urlpatterns = [
    url('^$', TimesheetDetailListView.as_view(), name='timesheetlist'),
    url('^timesheet/newlist/(?P<weekenddate>\d{4}-\d{2}-\d{2})/$', TimesheetListView.as_view(), name='timesheetlist-new'),
    url('^timesheet/(?P<pk>[0-9]+)/$',TimesheetDetailView.as_view(), name='timesheetdetail'),
    url('^timesheet/create/$',TimesheetCreateView.as_view(), name='timesheetcreate'),
    url('^timesheet/update/(?P<pk>[0-9]+)/$',TimesheetUpdateView.as_view(), name='timesheetupdate'),
    url('^timesheet/dataentry/$', timesheet_data_entry_view_test, name='ts-dataentry'),
    url('^timesheet/dataentry-formset/(?P<pk>[0-9]+)/$', timesheet_formset, name='ts-dataentry-formset'),
    url('^timesheet/test-formset/(?P<pk>[0-9]+)/(?P<weekenddate>\d{4}-\d{2}-\d{2})/$', test_formset_initial_data, name='ts-test-formset'),
    url('^timesheet-extra-field/$', timesheet_with_extra_field, name='timesheet-with-extra-field'),
    url('^timesheetset/(?P<user_id>[0-9]+)/$', manage_timesheet, name='manage_timesheet'),
    url('^timesheetset1/(?P<timesheet_id>[0-9]+)/$', manage_timesheet1, name='manage_timesheet1'),
    url('^weekenddatelist/$', WeekendDateListView.as_view(), name='weekenddate-list'),
]
