import os
from datetime import datetime,timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myprojects.settings')

import django
django.setup()

import random
from django.contrib.auth.models import User
from timesheet.models import *
from project.models import Project
from timesheet.helper_functions import dategenerator
from faker import Faker

fakegen = Faker('en_AU')
#
# for entry in range(20):
#     User.objects.get_or_create(username=fakegen.last_name_female(), password='qwerasdf')
#
# weekend_date = datetime.strptime('2017-01-04', '%Y-%m-%d')
# for entry in range(52):
#     WeekendDate.objects.get_or_create(weekenddate=weekend_date)
#     weekend_date = weekend_date + timedelta(weeks=1)

# project_list = ['17-001','17-002','17-003','17-004','17-005','17-006','17-007','17-008','17-009']
# for proj in project_list:
#     Project.objects.get_or_create(project_code=proj)


# workcode_dict= {'Normal': 10,
#                 'RnR': 80,
#                 'Annual Leave': 20,
#                 'Personal Leave': 21,
#                 'Carers Leave': 25,
#                 'Long Service Leave': 26,
#                 'Night Shift': 13,
#                 'Afternoon Shift': 14,
#                 'Bus Driving': 71,
#                 'Work Comp': 22}
#
# for wc in workcode_dict.keys():
#     # print(wc)
#     # print(workcode_dict[wc])
#     Workcode.objects.get_or_create(workcode_description=wc,workcode=workcode_dict[wc] )

# weekend_list = WeekendDate.objects.filter(weekenddate__lte='2017-05-01')
# emp_list = Employee.objects.all()
#
# for we in weekend_list:
#     for emp in emp_list:
#         Timesheet.objects.get_or_create(employee=emp, weekenddate=we)

# timesheets = Timesheet.objects.all()
# workcodes = Workcode.objects.all()
# projects = Project.objects.all()
#
# for ts in timesheets:
#     datelist = dategenerator(str(ts.weekenddate))
#     # print(datelist)
#     for date in datelist:
#         TimesheetDetail.objects.get_or_create(timesheet=ts,
#                                           workcode=random.choice(workcodes),
#                                           project=random.choice(projects),
#                                           workdate=date['workdate'],
#                                           hours=12)
