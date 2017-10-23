from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from project.models import Project
# Create your models here.
class Workcode(models.Model):
    workcode = models.PositiveSmallIntegerField()
    workcode_description = models.CharField(max_length=20)
    workcode_short = models.CharField(max_length=4)
    workcode_serial = models.SmallIntegerField()

    def __str__(self):
        return ('{} {} ({})').format(self.workcode_serial, self.workcode_short, self.workcode)


class WeekendDate(models.Model):
    weekenddate = models.DateField(unique=True)
    current_weekenddate = models.BooleanField(default=False)

    def __str__(self):
        return str(self.weekenddate)

class Timesheet(models.Model):
    employee = models.ForeignKey(User)
    weekenddate = models.ForeignKey(WeekendDate)

    class Meta:
        unique_together = ('employee', 'weekenddate')


    def __str__(self):
        return ('({}) {} --> {}').format(self.id, self.employee.username, self.weekenddate)



class TimesheetDetail(models.Model):
    timesheet = models.ForeignKey(Timesheet)
    workcode = models.ForeignKey(Workcode)
    project = models.ForeignKey('project.Project')
    workdate = models.DateField()
    hours = models.PositiveSmallIntegerField()

    def __str__(self):
        return ('{} __ {} __ {} __ {} __ {}H').format(self.timesheet.employee.username,self.workdate,self.project, self.workcode, self.hours)

    def get_absolute_url(self):
        return reverse('timesheet:timesheetdetail', kwargs={'pk':self.pk})

    class Meta:
        unique_together = ('timesheet','workcode','project','workdate')
