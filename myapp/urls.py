from django.conf.urls import url
from . import views, loader

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^update', loader.load, name='main'),
]