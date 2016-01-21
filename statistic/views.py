import logging

import simplejson as simplejson
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from statistic import controller

from statistic.models import Activedevicelog, AnalyzeRecord, UserSurvival, Deviceemaillog, Userconfiglog

logger = logging.getLogger(__name__)

@login_required
def index(request):
    return user_survivals(request)


@login_required
def user_survivals_origin(request):
    request_date = __get_request_date(request)
    interval_unit = __get_request_interval_unit(request)

    return __user_survivals_origin(request, request_date, interval_unit)


def __get_request_date(request):
    request_date_str = None
    if request.POST:
        request_date_str = request.POST.get('date')
    else:
        request_date_str = request.GET.get('date')

    request_date = None
    if request_date_str is not None:
        time_array = timezone.datetime.strptime(request_date_str, '%Y-%m-%d').timetuple()
        request_date = timezone.datetime(time_array[0], time_array[1], time_array[2], tzinfo=get_current_timezone())
    if request_date is None:
        request_date = timezone.now()
    return request_date


def __get_request_interval_unit(request):
    '''
    :return: 1 day, 2 week, 3 month
    '''
    return request.POST.get('interval_unit', 1)


@login_required
def user_survivals(request):
    request_date = __get_request_date(request)
    interval_unit = __get_request_interval_unit(request)
    user_survivals_data = controller.get_user_survivals_origin(request_date, interval_unit)

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

    return render(request, 'statistic/user_survivals.html', {'survivals': user_survivals_data,
                                                             'date': request_date.strftime('%Y-%m-%d'),
                                                             'survival_count': survival_count,
                                                             'unit': interval_unit})


def __user_survivals_origin(request, date, interval_unit):
    user_survivals_data = controller.get_user_survivals_origin(date, interval_unit)

    return render(request, 'statistic/user_survivals_origin.html',
                  {'survivals': user_survivals_data, 'date': date.strftime('%Y-%m-%d'), 'unit': interval_unit})

@login_required
def get_lost(request):
    request_date = __get_request_date(request)
    interval_unit = __get_request_interval_unit(request)

    user_survivals_data = controller.get_user_survivals_origin(request_date, interval_unit)

    lost_data = controller.analyze_lost(user_survivals_data)

    lost_data['date'] = request_date
    lost_data['interval_unit'] = interval_unit

    return JsonResponse(lost_data)

@login_required
def config_detail(request):
    imei = request.GET['imei']
    config_logs = Userconfiglog.objects.filter(imei=imei).select_related('incomingconfig', 'outgoingconfig')
    configs = []
    for config in config_logs:
        configs.append({'issuccess': config.issuccess,
                        'errormessage': config.errormessage,
                        'auto': config.isautoconfig,
                        'imei': config.imei,
                        'email': config.email,
                        'protocol': config.protocol,
                        'loginname': config.loginname,
                        'incomingconfig': {'address': config.incomingconfig.address,
                                           'port': config.incomingconfig.port,
                                           'security': config.incomingconfig.security},
                        'outgoingconfig': {'address': config.outgoingconfig.address,
                                           'port': config.outgoingconfig.port,
                                           'security': config.outgoingconfig.security}})

    return JsonResponse({'configs': configs})
