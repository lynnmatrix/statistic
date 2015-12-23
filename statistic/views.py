import logging

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from statistic.models import Activedevicelog, AnalyzeRecord, UserSurvival

logger = logging.getLogger(__name__)


def index(request):
	return user_survivals(request)


def user_survivals_origin(request):
	request_date = __get_request_date(request)

	return __user_survivals_origin(request, request_date)


def __get_request_date(request):
	request_date_str = request.POST.get('date')
	request_date = None
	if request_date_str is not None:
		time_array = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').timetuple();
		request_date = timezone.datetime(time_array[0], time_array[1], time_array[2], tzinfo=get_current_timezone())
	if request_date is None:
		request_date = timezone.now()
	return request_date


def user_survivals(request):
	request_date = __get_request_date(request)
	user_survivals_data = __get_user_survivals_origin(request_date)
	return render(request, 'statistic/user_survivals.html', {'survivals': user_survivals_data, 'date': request_date.strftime('%Y-%m-%d')})


def __user_survivals_origin(request, date):
	user_survivals_data = __get_user_survivals_origin(date)
	return render(request, 'statistic/user_survivals_origin.html', {'survivals': user_survivals_data, 'date': date.strftime('%Y-%m-%d')})


def __get_user_survivals_origin(date):
	__analyze_survival()

	date = timezone.localtime(date)
	date_array = date.timetuple()
	date = timezone.datetime(date_array[0], date_array[1], date_array[2], tzinfo=get_current_timezone())

	user_survivals = UserSurvival.objects.filter(firsttime__range=[date, date + timezone.timedelta(days=1)])
	return user_survivals


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
