
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^weatherchart/$', views.weatherchart, name='weatherchart'),
]