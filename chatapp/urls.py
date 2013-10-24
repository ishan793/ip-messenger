from django.conf.urls import patterns, url

from chatapp import views

urlpatterns = patterns('',
    #url(r'^$', views.index),
    url(r'^authenticate/$', views.Authenticate),
)
