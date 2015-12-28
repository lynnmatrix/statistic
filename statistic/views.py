import logging
from sets import Set

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from monthdelta import monthdelta

from statistic.models import Activedevicelog, AnalyzeRecord, UserSurvival, Deviceemaillog, Userconfiglog

logger = logging.getLogger(__name__)


def index(request):
	return user_survivals(request)


def user_survivals_origin(request):
	request_date = __get_request_date(request)
	interval_unit = __get_request_interval_unit(request)

	return __user_survivals_origin(request, request_date, interval_unit)


def __get_request_date(request):
	request_date_str = request.POST.get('date')
	request_date = None
	if request_date_str is not None:
		time_array = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').timetuple()
		request_date = timezone.datetime(time_array[0], time_array[1], time_array[2], tzinfo=get_current_timezone())
	if request_date is None:
		request_date = timezone.now()
	return request_date


def __get_request_interval_unit(request):
	'''
	:return: 1 day, 2 week, 3 month
	'''
	return request.POST.get('interval_unit', 1)


def user_survivals(request):
	request_date = __get_request_date(request)
	interval_unit = __get_request_interval_unit(request)
	user_survivals_data = __get_user_survivals_origin(request_date, interval_unit)

	logger.info("count %d", len(user_survivals_data))

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
															 'survival_count': survival_count,
															 'unit': interval_unit})


def __user_survivals_origin(request, date, interval_unit):
	user_survivals_data = __get_user_survivals_origin(date, interval_unit)

	return render(request, 'statistic/user_survivals_origin.html',
				  {'survivals': user_survivals_data, 'date': date.strftime('%Y-%m-%d'), 'unit': interval_unit})


def __get_user_survivals_origin(date, interval_unit):
	__analyze_survival()

	date = timezone.localtime(date)
	date_array = date.timetuple()
	date = timezone.datetime(date_array[0], date_array[1], date_array[2], tzinfo=get_current_timezone())

	date_range_end = date + timezone.timedelta(days=1)
	if '1' == interval_unit:
		pass
	elif '2' == interval_unit:
		weekday = date.weekday()
		date = date - timezone.timedelta(days=weekday)
		date_range_end = date + timezone.timedelta(days=7)
	elif '3' == interval_unit:
		month_day = date.day()
		date = date - timezone.timedelta(days=month_day)
		date_range_end = date + monthdelta(1)

	user_survivals_data = UserSurvival.objects.filter(firsttime__range=[date, date_range_end])
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
		except UserSurvival.MultipleObjectsReturned:
			user_survival_dup = UserSurvival.objects.filter(imei=log.imei)
			user_survival = user_survival_dup[0]
			logger.error("duplicate user survival %r", user_survival)
			for survival in user_survival_dup[1:]:
				survival.delete()

		if user_survival is None:
			user_survival = UserSurvival(imei=log.imei, firsttime=log.time)

		user_survival.lasttime = log.time
		user_survival.save()

	if device_logs.count() > 0:
		analyze_record.save()


def lost_next_day(request):
	request_date = __get_request_date(request)
	interval_unit = __get_request_interval_unit(request)
	user_survivals_data = __get_user_survivals_origin(request_date, interval_unit)

	logger.info("lost next day count %d", len(user_survivals_data))
	users_lost = []
	for user_survival in user_survivals_data:
		if user_survival.survival_day() is False:
			users_lost.append(user_survival.imei)

	logger.info("user lost %d", len(user_survivals_data))

	user_lost_cause_failure = {}
	user_emails = {}
	all_fail_count = 0
	for user_lost in users_lost:
		fail = Deviceemaillog.objects.filter(imei=user_lost).count() <= 0
		if fail:
			all_fail_count += 1
			user_lost_cause_failure[user_lost] = True
		else:
			user_lost_cause_failure[user_lost] = False

		user_emails[user_lost] = {'success': [], 'fail': []}

	config_logs = Userconfiglog.objects.filter(imei__in=users_lost)

	for config_log in config_logs:
		if config_log.issuccess:
			user_emails[config_log.imei]['success'].append(config_log.email)
		else:
			user_emails[config_log.imei]['fail'].append(config_log.email)

	all_fail_qq_163 = 0
	all_success_count = 0
	all_success_and_single_mailbox_count = 0

	for user, all_fail in user_lost_cause_failure.iteritems():
		if all_fail:
			for email in user_emails[user]['fail']:
				if email.find('qq.com') != -1 or email.find('163.com') != -1 or email.find('126.com') != -1:
					all_fail_qq_163 += 1
					break
		else:
			success_mailboxes = Set()
			fail_mailboxes = Set()
			for email in user_emails[user]['success']:
				success_mailboxes.add(email)
			for email in user_emails[user]['fail']:
				fail_mailboxes.add(email)

			if success_mailboxes.issuperset(fail_mailboxes):
				all_success_count += 1
				if len(success_mailboxes) == 1:
					all_success_and_single_mailbox_count += 1


	return render(request, "statistic/lost.html", {'date': request_date,
												   'unit': interval_unit,
												   'lost': user_lost_cause_failure,
												   'ratio': {'total': len(user_lost_cause_failure),
															 'all_fail': all_fail_count,
															 'all_fail_qq_163': all_fail_qq_163,
															 'all_success': all_success_count,
															 'all_success_and_single_mailbox_count': all_success_and_single_mailbox_count
															 },
												   'user_emails': user_emails
												   })
