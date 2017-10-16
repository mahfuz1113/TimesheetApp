from django.conf.urls import url
from .views import *

app_name = 'modalform'
urlpatterns = [
    url('^$',CarListView.as_view(), name='carlistview'),
    url('^create/$',CarCreateView.as_view(), name='carcreateview'),
    url('^update/(?P<pk>[0-9]+)$',CarUpdateView.as_view(), name='carupdateview'),
    url('^delete/(?P<pk>[0-9]+)$',CarDeleteView.as_view(), name='cardeleteview'),
    url('^inlineformset/(?P<owner_id>[0-9]+)$',CarInlineFormSetView, name='carinlineformset'),

]
