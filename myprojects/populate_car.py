import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myprojects.settings')

import django
django.setup()

import random
from modalform.models import *
from faker import Faker

fakegen = Faker('en_AU')


#
# for entry in range(5):
#     Owner.objects.get_or_create(name=fakegen.name())

owners = Owner.objects.all()
make_list = ['Toyota', 'Ford', 'Holden', 'BMW']
model_list = ['Camry', 'Corolla', 'Pajero', 'Prado', 'Barina', 'Commodor', 'Falcon']

for entry in range(10):
    Car.objects.get_or_create(
                make = random.choice(make_list),
                model = random.choice(model_list),
                door = random.randrange(2,6+1),
                owner = random.choice(owners),
                price=random.randrange(5000,30000+1)
    )
