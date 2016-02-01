#!/usr/bin/env python
# coding:utf-8
from django.utils import timezone
from django.utils.timezone import get_current_timezone


def trim_2_local_day_start(date):
    """
    转换成对应local time的当天起始时间
    """
    trim_date = timezone.localtime(date)
    date_array = trim_date.timetuple()
    trim_date = timezone.datetime(date_array[0], date_array[1], date_array[2], tzinfo=get_current_timezone())
    return trim_date


def week_start(date):
    weekday = date.weekday()
    monday = date - timezone.timedelta(days=weekday)
    return day_start(monday)


def month_start(date):
    return timezone.datetime(year=date.year, month=date.month, day=1, tzinfo=date.tzinfo)


def day_start(day):
    return timezone.datetime(year=day.year, month=day.month, day=day.day, tzinfo=day.tzinfo)
