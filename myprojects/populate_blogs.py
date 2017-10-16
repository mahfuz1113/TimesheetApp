import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myprojects.settings')

import django
django.setup()


import random
from modalform.models import *
from faker import Faker

fakegen = Faker('en_AU')

# author_list = []
# for entry in range(10):
#     author_list.append(fakegen.name())


for entry in range(10):
    Author.objects.get_or_create(name=fakegen.name(), email=fakegen.email())

def blog_create():
    b = Blog.objects.get_or_create(name=fakegen.name(), tagline=fakegen.sentence())[0]
    b.save()
    return b


def populate(N=5):

    for entry in range(N):
        fake_headline = fakegen.sentence()
        fake_body_text = fakegen.text()
        fake_pub_date = fakegen.date_this_decade(before_today=True, after_today=True)
        fake_mod_date = fakegen.date_this_decade(before_today=True, after_today=True)
        fake_n_comments = random.randrange(10,99,1)
        fake_n_pingbacks = random.randrange(10,99,1)
        fake_rating = random.randrange(0,5,1)

        fake_blog = blog_create()
        fake_author = Author.objects.all()

        entry_add = Entry.objects.get_or_create(blog=fake_blog,
                                    headline=fake_headline,
                                    body_text=fake_body_text,
                                    pub_date=fake_pub_date,
                                    mod_date=fake_mod_date,
                                    n_comments=fake_n_comments,
                                    n_pingbacks=fake_n_pingbacks,
                                    rating=fake_rating)[0]

        entry_add.save()
        entry_add.authors.add(random.choice(fake_author))

if __name__ == '__main__':
    print('Creating Fake Data')
    populate(1000)
    print('Data population completed!')
