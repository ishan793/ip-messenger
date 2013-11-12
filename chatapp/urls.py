from django.conf.urls import patterns, url

from chatapp import views

urlpatterns = patterns('',
    #url(r'^$', views.index),
    url(r'^authenticate/$', views.Authenticate),
    url(r'^signup/$', views.register_user),
	url(r'^flush/$', views.flush_all_presence),
	url(r'^onpre/$', views.online_presence),
	url(r'^onpresave/$', views.save_to_onpre),
    
)
