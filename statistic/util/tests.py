#!/usr/bin/env python
# coding:utf-8
from django.test import TestCase
from django.utils import timezone

from statistic.util.datehelper import month_start


class Test(TestCase):
    def test_month_start(self):
        first_day = month_start(timezone.now())
        self.assertEqual(1, first_day.day)

