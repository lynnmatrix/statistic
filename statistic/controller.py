import logging
from sets import Set

import monthdelta as monthdelta
from django.utils import timezone

from statistic.models import UserSurvival, AnalyzeRecord, Activedevicelog, Userconfiglog
from statistic.util.datehelper import trim_2_local_day_start

logger = logging.getLogger(__name__)


def get_user_survivals_origin(date, interval_unit):
    analyze_survival()

    date = trim_2_local_day_start(date)

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
    return user_survivals_data.order_by('-lasttime')


def analyze_survival():
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
    i =0
    count = device_logs.count()
    for log in device_logs:
        logger.info("%d/%d", i, count)
        i +=1
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
            user_survival = UserSurvival(imei=log.imei, firsttime=log.time, lasttime=log.time)

        if log.time > user_survival.lasttime:
            user_survival.lasttime = log.time
        if log.time < user_survival.firsttime:
            user_survival.firsttime = log.time

        user_survival.save()

    if device_logs.count() > 0:
        analyze_record.save()


def analyze_lost(user_survivals_data):
    # logger.info("lost next day count %d", len(user_survivals_data))
    users_lost = []
    for user_survival in user_survivals_data:
        if user_survival.survival_day() is False:
            users_lost.append(user_survival.imei)

    # logger.info("user lost %d", len(users_lost))

    user_lost_cause_failure = {}
    user_config_logs = {}
    all_fail_count = len(users_lost)

    for user_lost in users_lost:
        user_lost_cause_failure[user_lost] = True
        user_config_logs[user_lost] = {'success': [], 'fail': []}

    config_logs = Userconfiglog.objects.filter(imei__in=users_lost)

    for config_log in config_logs:

        if config_log.issuccess:
            user_config_logs[config_log.imei]['success'].append(config_log.email)
            if user_lost_cause_failure[config_log.imei]:
                user_lost_cause_failure[config_log.imei] = False
                all_fail_count -= 1
        else:
            user_config_logs[config_log.imei]['fail'].append(config_log.email)

    # logger.info("%s", user_config_logs)
    # logger.info("%s", user_lost_cause_failure)

    all_fail_qq_163 = 0
    all_success_count = 0
    all_success_and_single_mailbox_count = 0

    for user, all_fail in user_lost_cause_failure.iteritems():
        if all_fail:
            for email in user_config_logs[user]['fail']:
                if email.find('qq.com') != -1 or email.find('163.com') != -1 or email.find('126.com') != -1:
                    all_fail_qq_163 += 1
                    break
        else:
            success_mailboxes = Set()
            fail_mailboxes = Set()
            for email in user_config_logs[user]['success']:
                success_mailboxes.add(email)
            for email in user_config_logs[user]['fail']:
                fail_mailboxes.add(email)

            if success_mailboxes.issuperset(fail_mailboxes):
                all_success_count += 1
                if len(success_mailboxes) == 1:
                    all_success_and_single_mailbox_count += 1

    result = {
        'lost': user_lost_cause_failure,
        'ratio': {'total': len(user_lost_cause_failure),
                  'all_fail': all_fail_count,
                  'all_fail_qq_163': all_fail_qq_163,
                  'all_success': all_success_count,
                  'all_success_and_single_mailbox_count': all_success_and_single_mailbox_count
                  },
        'user_config_logs': user_config_logs
    }
    # logger.info("result %s", result)
    return result
