#!/usr/bin/env python
# coding:utf-8
import logging

from dateutil.relativedelta import relativedelta

from statistic.models import UserSurvival
from statistic.util.datehelper import trim_2_local_day_start, week_start, month_start

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
    result = 0
    if 1 == group_window:
        delta = time - start_date
        result = delta.days
    if 2 == group_window:
        start_date = week_start(start_date)
        time = week_start(time)

        delta = time - start_date
        result = delta.days / 7
    elif 3 == group_window:
        start_date = month_start(start_date)
        time = month_start(time)

        result = (time.year - start_date.year) * 12 + (time.month - start_date.month)

    return result, time


def is_survival(user_survival, survival_interval):

    survival = False
    if 1 == survival_interval:
        survival = user_survival.survival_day()
    elif 2 == survival_interval:
        survival = user_survival.survival_week()
    elif 3 == survival_interval:
        survival = user_survival.survival_month()

    return survival
