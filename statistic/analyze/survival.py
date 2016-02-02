#!/usr/bin/env python
# coding:utf-8
import logging

from datetime import timedelta

from django.utils import timezone
from monthdelta import MonthDelta

from statistic.models import UserSurvival
from statistic.util.datehelper import week_start, month_start, day_start

logger = logging.getLogger(__name__)


def get_survival_rate_tendency(start_date, end_date, group_window, survival_interval):
    """
    指定时间段的留存率变化
    :param start_date: the start date to tendency
    :param end_date: the end date to tendency
    :param group_window: group new users in this window
    :return:[[date, total, survival], [date, total, survival),...], the item of array may be none. If the date is not none,
    the 'total' must greater than 0.
    """
    # start_date = trim_2_local_day_start(start_date)
    # end_date = trim_2_local_day_start(end_date)

    user_survivals_data = UserSurvival.objects.filter(firsttime__range=[start_date, end_date])
    x_length = cal_x_length(start_date, end_date, group_window)

    result = [None for x in range(x_length)]

    for survival in user_survivals_data:
        (index, index_start_date) = get_index(start_date, group_window, survival.firsttime)

        stat = result[index]
        if stat is None:
            stat = [index_start_date, 0, 0]
            result[index] = stat

        stat[1] += 1

        if is_survival(survival, survival_interval):
            stat[2] += 1

    return result


def cal_x_length(start_date, end_date, group_window):
    (index, _) = get_index(start_date, group_window, end_date)
    return index + 1


def get_index(start_date, group_window, time):
    index = 0
    if 1 == group_window:
        delta = time - start_date
        index = delta.days
    if 2 == group_window:
        start_date = week_start(start_date)
        time = week_start(time)

        delta = time - start_date
        index = delta.days / 7
    elif 3 == group_window:
        start_date = month_start(start_date)
        time = month_start(time)

        index = (time.year - start_date.year) * 12 + (time.month - start_date.month)

    return index, time


def is_survival(user_survival, survival_interval):
    survival = False
    if 1 == survival_interval:
        survival = user_survival.survival_day()
    elif 2 == survival_interval:
        survival = user_survival.survival_week()
    elif 3 == survival_interval:
        survival = user_survival.survival_month()

    return survival


def get_survival_rate(anchor_date, group_window=2, unit=2):
    start_time, end_time = window_range(anchor_date, group_window)

    user_survivals = UserSurvival.objects.filter(firsttime__range=[start_time, end_time])
    user_count = len(user_survivals)

    x_count = cal_x_length(start_time, timezone.now(), unit)

    values = [{'x': i, 'y': 0} for i in range(x_count)]
    for user_survival in user_survivals:
        index, _ = get_index(anchor_date, unit, user_survival.lasttime)
        values[index]['y'] += 1

    for index in range(x_count - 2, -1, -1):
        values[index]['y'] += values[index + 1]['y']

    return {
        'start_date': start_time,
        'user_window': group_window,
        'unit': unit,
        'values': values,
        'total': user_count
    }


def window_range(anchor_date, group_window):
    if 1 == group_window:
        start_time = day_start(anchor_date)
    elif 2 == group_window:
        start_time = week_start(anchor_date)
        end_time = start_time + timedelta(days=7)
    elif 3 == group_window:
        start_time = month_start(anchor_date)
        end_time = start_time + MonthDelta(months=1)

    return start_time, end_time
