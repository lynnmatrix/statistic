from django.conf.urls import url, include

from statistic import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^active$', views.active_users, name='active'),
]
