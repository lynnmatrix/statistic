import datetime
from django.shortcuts import render

# Create your views here.
from statistic.models import Activedevicelog


def index(request):
	day = datetime.date.today()
	return __active_users(request, day)


def active_users(request):
	request_date = request.POST.get('date')
	return __active_users(request, request_date)


def __active_users(request, date):
	request_date = request.POST.get('date')
	if request_date:
		date = request_date
	devicelogs = Activedevicelog.objects.exclude(umengchannel='debug');

	return render(request, 'statistic/index.html', {'logs': devicelogs, 'date':date})