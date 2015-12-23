import logging

import pytz
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from statistic.models import Activedevicelog, AnalyzeRecord, UserSurvival

logger = logging.getLogger(__name__)


def index(request):
	day = timezone.now()
	return __active_users(request, day)


def active_users(request):
	time_array = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').timetuple();
	request_date = timezone.datetime(time_array[0], time_array[1], time_array[2], tzinfo=get_current_timezone())
	return __active_users(request, request_date)


def __active_users(request, date):
	__analyze_survival()

	date = timezone.localtime(date)
	date_array = date.timetuple()
	date = timezone.datetime(date_array[0], date_array[1], date_array[2], tzinfo=get_current_timezone())

	user_survivals = UserSurvival.objects.filter(firsttime__range=[date, date + timezone.timedelta(days=1)])
	logger.info('%r', date)
	return render(request, 'statistic/index.html', {'survivals': user_survivals, 'date': date.strftime('%Y-%m-%d')})


def __analyze_survival():
	action_str = 'user_survival'
	try:
		analyze_record = AnalyzeRecord.objects.get(action__exact=action_str)
	except AnalyzeRecord.DoesNotExist:
		analyze_record = None

	device_logs = Activedevicelog.objects.exclude(umengchannel='debug')
	if analyze_record is not None:
		device_logs = device_logs.filter(time__gt=analyze_record.time)
	else:
		analyze_record = AnalyzeRecord(action=action_str)

	analyze_record.time = timezone.now()
	for log in device_logs:
		try:
			user_survival = UserSurvival.objects.get(imei=log.imei)
		except UserSurvival.DoesNotExist:
			user_survival = None

		if user_survival is None:
			user_survival = UserSurvival(imei=log.imei, firsttime=log.time)

		user_survival.lasttime = log.time
		user_survival.save()

	if device_logs.count() > 0:
		analyze_record.save()
