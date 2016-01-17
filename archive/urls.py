from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^([A-Z]{1}[0-9]{4})/$', views.splits, name='splits'),
]