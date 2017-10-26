from django.conf.urls import url
from .views import *
app_name='project'

urlpatterns=[
    url('^$', ProjectListView.as_view(), name='projectlist')
]
