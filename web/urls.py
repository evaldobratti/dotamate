from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url('^matches/(?P<match_id>\d+)/$', views.match_detail, name='match_detail'),

)