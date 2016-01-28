from django.conf.urls import url, include

from statistic import views
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^survival/$', views.user_survivals, name='survival'),
    url(r'^survival/origin', views.user_survivals_origin, name='survival_origin'),

    url(r'^get_survivals/$', views.get_survivals, name="get_survivals"),
    url(r'^get_lost/$', views.get_lost, name="get_lost"),
    url(r'^config/$', views.config_detail, name="config"),
]

