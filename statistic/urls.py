from django.conf.urls import url, include

from statistic import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^survival/$', views.user_survivals, name='survival'),
    url(r'^survival/origin', views.user_survivals_origin, name='survival_origin'),
    url(r'^lost/', views.lost_next_day, name='lost_next'),
    url(r'^get_lost/$', views.get_lost, name="get_lost"),
    # url(r'^all_fail_user'),
    # url(r'^config/(?P<imei>\w+)', views.config_detail, name="config_detail"),
]
