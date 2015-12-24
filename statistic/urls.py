from django.conf.urls import url, include

from statistic import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^survival/$', views.user_survivals, name='survival'),
	url(r'^survival/origin', views.user_survivals_origin, name='survival_origin'),
	url(r'^lost/', views.lost_next_day, name='lost_next'),
]
