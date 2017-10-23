import os
from datetime import datetime,timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myprojects.settings')

import django
django.setup()

import random
from django.contrib.auth.models import User
from project.models import *
from timesheet.helper_functions import dategenerator
from faker import Faker

fakegen = Faker('en_AU')

# project_list = ['17-001','17-002','17-003','17-004','17-005','17-006','17-007','17-008','17-009']

def create_project():
    network_list = {'Project 17-001':'M0A5FO017001',
                    'Project 17-002':'M0A5FO017002',
                    'Project 17-003':'M0A5FO017003',
                    'Project 17-004':'M0A5FO017004',
                    'Project 17-005':'M0A5FO017005',
                    'Project 17-006':'M0A5FO017006',
                    'Project 17-007':'M0A5FO017007',
                    'Project 17-008':'M0A5FO017008',
                    'Project 17-009':'M0A5FO017009',
                    'Project 17-010':'M0A5FO017010'}

    for k,v in network_list.items():
        Network.objects.get_or_create(description=k, code=v)

def create_project_status():
    project_status_list = {
                    'Not yet approved': 10,
                    'Approved':         20,
                    'Inprogress':       30,
                    'Completed':        40,
                    'Completed Inhouse':50,
                    'Closed':           60,
                    'Cancelled':        70,
                    'On Hold':          80,
                    'Posponded':        90
                    }

    for k,v in project_status_list.items():
        ProjectStatus.objects.get_or_create(description=k, code=v)


create_project_status()
