from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Workcode(models.Model):
    workcode = models.PositiveSmallIntegerField()
    workcode_description = models.CharField(max_length=20)
    workcode_short = models.CharField(max_length=4)
    workcode_serial = models.SmallIntegerField()

    def __str__(self):
        return ('{} {} ({})').format(self.workcode_serial, self.workcode_description, self.workcode)


class Project(models.Model):
    project = models.CharField(max_length=10)

    def __str__(self):
        return self.project

class Employee(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class WeekendDate(models.Model):
    weekenddate = models.DateField(unique=True)

    def __str__(self):
        return str(self.weekenddate)

class Timesheet(models.Model):
    employee = models.ForeignKey(Employee)
    weekenddate = models.ForeignKey(WeekendDate)

    class Meta:
        unique_together = ('employee', 'weekenddate')


    def __str__(self):
        return ('({}) {} --> {}').format(self.id, self.employee.name, self.weekenddate)



class TimesheetDetail(models.Model):
    timesheet = models.ForeignKey(Timesheet)
    workcode = models.ForeignKey(Workcode)
    project = models.ForeignKey(Project)
    workdate = models.DateField()
    hours = models.PositiveSmallIntegerField()

    def __str__(self):
        return ('{} // {} // {}H').format(self.timesheet.employee.name,self.workdate,self.hours)

    def get_absolute_url(self):
        return reverse('timesheet:timesheetdetail', kwargs={'pk':self.pk})
