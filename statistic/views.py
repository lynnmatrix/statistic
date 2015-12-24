import logging

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from statistic.models import Activedevicelog, AnalyzeRecord, UserSurvival, Deviceemaillog

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
		time_array = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').timetuple()
		request_date = timezone.datetime(time_array[0], time_array[1], time_array[2], tzinfo=get_current_timezone())
	if request_date is None:
		request_date = timezone.now()
	return request_date


def user_survivals(request):
	request_date = __get_request_date(request)
	user_survivals_data = __get_user_survivals_origin(request_date)

	# [total, day,week,month,year, last_week]
	survival_count = [0, 0, 0, 0, 0, 0]

	for user_survival in user_survivals_data:
		survival_count[0] += 1
		if user_survival.survival_day():
			survival_count[1] += 1
			if user_survival.survival_week():
				survival_count[2] += 1
				if user_survival.survival_month():
					survival_count[3] += 1
					if user_survival.survival_year():
						survival_count[4] += 1

		if user_survival.survival_last_week():
			survival_count[5] += 1

	logger.info("%r", survival_count)

	return render(request, 'statistic/user_survivals.html', {'survivals': user_survivals_data,
															 'date': request_date.strftime('%Y-%m-%d'),
															 'survival_count': survival_count})


def __user_survivals_origin(request, date):
	user_survivals_data = __get_user_survivals_origin(date)

	return render(request, 'statistic/user_survivals_origin.html',
				  {'survivals': user_survivals_data, 'date': date.strftime('%Y-%m-%d')})


def __get_user_survivals_origin(date):
	__analyze_survival()

	date = timezone.localtime(date)
	date_array = date.timetuple()
	date = timezone.datetime(date_array[0], date_array[1], date_array[2], tzinfo=get_current_timezone())

	user_survivals_data = UserSurvival.objects.filter(firsttime__range=[date, date + timezone.timedelta(days=1)])
	return user_survivals_data.order_by('lasttime').reverse()


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


def lost_next_day(request):
	request_date = __get_request_date(request)
	user_survivals_data = __get_user_survivals_origin(request_date)

	users_lost = []
	for user_survival in user_survivals_data:
		if user_survival.survival_day() is False:
			users_lost.append(user_survival.imei)

	logger.info("%r", users_lost)

	user_lost_cause_failure = {}
	failure_count = 0
	for user_lost in users_lost:
		fail = Deviceemaillog.objects.filter(imei=user_lost).count() <= 0
		if fail:
			failure_count += 1
			user_lost_cause_failure[user_lost] = True
		else:
			user_lost_cause_failure[user_lost] = False
			
	logger.info("failure %r", user_lost_cause_failure)

	return render(request, "statistic/lost.html", {'date': request_date,
												   'lost': user_lost_cause_failure,
												   'ratio': {'total': len(user_lost_cause_failure),
															 'failure_count': failure_count
															 }
												   })
