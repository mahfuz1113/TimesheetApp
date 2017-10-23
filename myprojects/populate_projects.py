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

# project_list = ['17-001','17-002','17-003','17-004','17-005','17-006','17-007','17-008','17-009']

network_list = [{'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'},
                {'Project 17-001':'M0A5FO017001'}]

for k,v in network_list:
    Project.objects.get_or_create(description=k, code=v)
