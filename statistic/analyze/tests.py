#!/usr/bin/env python
# coding:utf-8
import logging
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from statistic.analyze.survival import cal_x_length, get_survival_rate_tendency, get_survival_rate
from statistic.util.datehelper import month_start, week_start
from statistic.models import UserSurvival

logger = logging.getLogger(__name__)


class Test(TestCase):
    def setUp(self):
        self.day1 = month_start(timezone.now() - timedelta(days=60))

        self.day2 = self.day1 + timedelta(days=1)
        self.day_next_week_1 = self.day1 + timedelta(days=7)
        self.day_next_week_2 = self.day2 + timedelta(days=7)
        self.day_next_month_1 = self.day1 + relativedelta(months=1)
        self.day_next_month_2 = self.day2 + relativedelta(months=1)

        UserSurvival.objects.create(imei='imei1', firsttime=self.day1, lasttime=self.day1)
        UserSurvival.objects.create(imei='imei2', firsttime=self.day1, lasttime=self.day2)
        UserSurvival.objects.create(imei='imei3', firsttime=self.day2, lasttime=self.day_next_month_2)
        UserSurvival.objects.create(imei='imei4', firsttime=self.day2, lasttime=self.day_next_week_1)

    def test_cal_x_length(self):
        self.assertTrue(cal_x_length(self.day1, self.day_next_month_2, 2), 2)

    def test_get_survival_rate_tendency(self):
        result = get_survival_rate_tendency(self.day1, self.day2, 1, 1)
        self.assertEqual(2, len(result))
        self.assertEqual(2, result[0][1])
        self.assertEqual(1, result[0][2])
        self.assertEqual(2, result[1][1])
        self.assertEqual(2, result[1][2])

        result = get_survival_rate_tendency(self.day1, self.day_next_month_2, 2, 3)
        self.assertEqual(5, len(result))
        self.assertEqual(4, result[0][1])
        self.assertEqual(1, result[0][2])
        self.assertIsNone(result[1])
        self.assertIsNone(result[2])
        self.assertIsNone(result[3])
        self.assertIsNone(result[4])


class TestSurvivalRate(TestCase):
    def setUp(self):
        self.day1 = week_start(timezone.now() - timedelta(days=60))

        self.day2 = self.day1 + timedelta(days=1)
        self.day_next_week_1 = self.day1 + timedelta(days=7)
        self.day_next_week_2 = self.day2 + timedelta(days=7)
        self.day_next_month_1 = self.day1 + relativedelta(months=1)
        self.day_next_month_2 = self.day2 + relativedelta(months=1)

        UserSurvival.objects.create(imei='imei1', firsttime=self.day1, lasttime=self.day1)
        UserSurvival.objects.create(imei='imei2', firsttime=self.day1, lasttime=self.day2)
        UserSurvival.objects.create(imei='imei3', firsttime=self.day2, lasttime=self.day_next_month_2)
        UserSurvival.objects.create(imei='imei4', firsttime=self.day2, lasttime=self.day_next_week_2)

    def test_get_survival_rate(self):
        result = get_survival_rate(self.day1, 2, 2)
        self.assertEqual(2, result['unit'])
        self.assertEqual(2, result['user_window'])
        self.assertEqual(week_start(self.day1), result['start_date'])
        self.assertEqual(4, result['total'])

        values = result['values']
        self.assertEqual(4, values[0]['y'])
        self.assertEqual(2, values[1]['y'])
        self.assertEqual(1, values[2]['y'])
        self.assertEqual(1, values[3]['y'])
        self.assertEqual(1, values[4]['y'])
        for x in range(5, 10):
            self.assertEqual(0, values[x]['y'])
