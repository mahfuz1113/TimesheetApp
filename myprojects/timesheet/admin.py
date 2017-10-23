from django.contrib import admin
from .models import *
# Register your models here.

class TimesheetDetailAdmin(admin.ModelAdmin):
    search_fields = ['timesheet__weekenddate__weekenddate']

    list_filter = ['timesheet__employee','timesheet__weekenddate__weekenddate']


# admin.site.register(Project)
admin.site.register(TimesheetDetail, TimesheetDetailAdmin)
admin.site.register(Workcode)
admin.site.register(Timesheet)
admin.site.register(WeekendDate)
