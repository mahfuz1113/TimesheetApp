from django.conf.urls import url
from .views import manage_children

app_name = 'nestedformset'

urlpatterns = [
    url('^(?P<parent_id>[0-9]+)/$', manage_children, name='nestedformset'),
]
