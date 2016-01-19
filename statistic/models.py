# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from datetime import timedelta

from django.db import models
from django.utils import timezone
from monthdelta import MonthDelta


class Activedevicelog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50)  # Field name made lowercase.
    umengdeviceinfo = models.CharField(db_column='UmengDeviceInfo', max_length=120, blank=True,
                                       null=True)  # Field name made lowercase.
    umengchannel = models.CharField(db_column='UmengChannel', max_length=20, blank=True,
                                    null=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ActiveDeviceLog'


class Autodomainconfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domainconfigidx = models.ForeignKey('Domainconfig', models.DO_NOTHING,
                                        db_column='DomainConfigIdx')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AutoDomainConfig'


class Changehistoryoffilter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=500)  # Field name made lowercase.
    guid = models.CharField(db_column='GUID', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChangeHistoryOfFilter'


class Configinfo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    security = models.IntegerField(db_column='Security')  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50, blank=True, null=True)  # Field name made lowercase.
    displayname = models.CharField(db_column='DisplayName', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    enablemesg = models.TextField(db_column='EnableMesg', blank=True,
                                  null=True)  # Field name made lowercase. This field type is a guess.
    enableurl = models.TextField(db_column='EnableUrl', blank=True,
                                 null=True)  # Field name made lowercase. This field type is a guess.
    certid = models.ForeignKey('Domaincert', models.DO_NOTHING, db_column='CertId', blank=True,
                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ConfigInfo'


class Deviceemaillog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    protocol = models.CharField(db_column='Protocol', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    osversion = models.IntegerField(db_column='OsVersion', blank=True, null=True)  # Field name made lowercase.
    appversion = models.CharField(db_column='AppVersion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DeviceEmailLog'


class Domaincert(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    cert = models.TextField(db_column='Cert', blank=True,
                            null=True)  # Field name made lowercase. This field type is a guess.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    host = models.CharField(db_column='Host', max_length=50, blank=True, null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DomainCert'


class Domainconfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    incomingconfig = models.ForeignKey(Configinfo, models.DO_NOTHING, db_column='IncomingConfig',
                                       related_name='domain_incoming_config')  # Field name made lowercase.
    outgoingconfig = models.ForeignKey(Configinfo, models.DO_NOTHING, db_column='OutgoingConfig',
                                       related_name='domain_outgoing_config')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DomainConfig'


class Domainwelcome(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    easwelcome = models.CharField(db_column='EASWelcome', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.
    imapwelcome = models.CharField(db_column='IMAPWelcome', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    popwelcome = models.CharField(db_column='POPWelcome', max_length=100, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DomainWelcome'


class Domainwhitelist(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    host = models.CharField(db_column='Host', max_length=100)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DomainWhiteList'


class Emaillog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EmailLog'


class Filterconfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=50)  # Field name made lowercase.
    enable = models.IntegerField(db_column='Enable')  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    appversion = models.IntegerField(db_column='AppVersion', blank=True, null=True)  # Field name made lowercase.
    jsonguid = models.CharField(db_column='JsonGuid', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FilterConfig'


class Filterfile(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=50)  # Field name made lowercase.
    enable = models.IntegerField(db_column='Enable')  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    appversion = models.IntegerField(db_column='AppVersion', blank=True, null=True)  # Field name made lowercase.
    jsonguid = models.CharField(db_column='JsonGuid', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FilterFile'


class Filteruserrequest(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    reporttime = models.DateTimeField(db_column='ReportTime')  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    isrelease = models.IntegerField(db_column='IsRelease')  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    file = models.CharField(db_column='File', max_length=100)  # Field name made lowercase.
    descript = models.CharField(db_column='Descript', max_length=200, blank=True,
                                null=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50, blank=True, null=True)  # Field name made lowercase.
    osversion = models.IntegerField(db_column='OsVersion', blank=True, null=True)  # Field name made lowercase.
    appversion = models.IntegerField(db_column='AppVersion', blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FilterUserRequest'


class Junksender(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    senderemail = models.CharField(db_column='SenderEmail', max_length=90)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JunkSender'


class Latestemailconfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    reporttime = models.DateTimeField(db_column='ReportTime', blank=True, null=True)  # Field name made lowercase.
    incomingconfig = models.ForeignKey('Userconfiginfo', models.DO_NOTHING, db_column='IncomingConfig',
                                       related_name='latest_incoming_config')  # Field name made lowercase.
    outgoingconfig = models.ForeignKey('Userconfiginfo', models.DO_NOTHING, db_column='OutgoingConfig',
                                       related_name='latest_outgoing_config')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LatestEmailConfig'


class Mx2Domain(models.Model):
    mx = models.CharField(db_column='MX', primary_key=True, max_length=100)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MX2Domain'


class Proxyconfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    version = models.IntegerField(db_column='Version')  # Field name made lowercase.
    type = models.IntegerField()
    address = models.CharField(db_column='Address', max_length=100)  # Field name made lowercase.
    originaddress = models.CharField(db_column='OriginAddress', max_length=100, blank=True,
                                     null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    originport = models.IntegerField(db_column='OriginPort', blank=True, null=True)  # Field name made lowercase.
    usessl = models.IntegerField(db_column='UseSSL', blank=True, null=True)  # Field name made lowercase.
    usetsl = models.IntegerField(db_column='UseTSL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProxyConfig'


class Userapplog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=100, blank=True, null=True)  # Field name made lowercase.
    emaillist = models.TextField(db_column='EmailList', blank=True, null=True)  # Field name made lowercase.
    logpath = models.CharField(db_column='LogPath', max_length=200)  # Field name made lowercase.
    filename = models.CharField(db_column='FileName', max_length=100, blank=True,
                                null=True)  # Field name made lowercase.
    uploadtime = models.DateTimeField(db_column='UploadTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserAppLog'


class Userconfiginfo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    protocol = models.IntegerField(db_column='Protocol')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=50)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port')  # Field name made lowercase.
    security = models.IntegerField(db_column='Security')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserConfigInfo'


class Userconfiglog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    isautoconfig = models.IntegerField(db_column='IsAutoConfig')  # Field name made lowercase.
    issuccess = models.IntegerField(db_column='IsSuccess')  # Field name made lowercase.
    isrelease = models.IntegerField(db_column='IsRelease')  # Field name made lowercase.
    errormessage = models.TextField(db_column='ErrorMessage', blank=True,
                                    null=True)  # Field name made lowercase. This field type is a guess.
    protocol = models.IntegerField(db_column='Protocol')  # Field name made lowercase.
    incomingconfig = models.ForeignKey(Userconfiginfo, models.DO_NOTHING, db_column='IncomingConfig',
                                       related_name='log_incoming_config')  # Field name made lowercase.
    outgoingconfig = models.ForeignKey(Userconfiginfo, models.DO_NOTHING, db_column='OutgoingConfig',
                                       related_name='log_outgoing_config')  # Field name made lowercase.
    loginname = models.CharField(db_column='LoginName', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    reporttime = models.DateTimeField(db_column='ReportTime')  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50, blank=True, null=True)  # Field name made lowercase.
    osversion = models.IntegerField(db_column='OsVersion', blank=True, null=True)  # Field name made lowercase.
    isfirstlogin = models.IntegerField(db_column='IsFirstLogin', blank=True, null=True)  # Field name made lowercase.
    freshappversion = models.CharField(db_column='FreshAppVersion', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    freshappchannel = models.CharField(db_column='FreshAppChannel', max_length=50, blank=True,
                                       null=True)  # Field name made lowercase.
    appversion = models.CharField(db_column='AppVersion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    network = models.CharField(db_column='Network', max_length=50, blank=True, null=True)  # Field name made lowercase.
    task = models.CharField(db_column='Task', max_length=36, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserConfigLog'


class Userconfigtask(models.Model):
    id = models.CharField(db_column='Id', primary_key=True, max_length=36)  # Field name made lowercase.
    domain = models.CharField(db_column='Domain', max_length=50)  # Field name made lowercase.
    protocol = models.IntegerField(db_column='Protocol')  # Field name made lowercase.
    login = models.CharField(db_column='Login', max_length=50)  # Field name made lowercase.
    incomingaddress = models.CharField(db_column='IncomingAddress', max_length=50)  # Field name made lowercase.
    incomingport = models.IntegerField(db_column='IncomingPort')  # Field name made lowercase.
    incomingsecurity = models.IntegerField(db_column='IncomingSecurity')  # Field name made lowercase.
    outgoingaddress = models.CharField(db_column='OutgoingAddress', max_length=50)  # Field name made lowercase.
    outgoingport = models.IntegerField(db_column='OutgoingPort')  # Field name made lowercase.
    outgoingsecurity = models.IntegerField(db_column='OutgoingSecurity')  # Field name made lowercase.
    currentconfig = models.TextField(db_column='CurrentConfig', blank=True,
                                     null=True)  # Field name made lowercase. This field type is a guess.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    tasktime = models.DateTimeField(db_column='TaskTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserConfigTask'


class Userhelplog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    otheremail = models.CharField(db_column='OtherEmail', max_length=200, blank=True,
                                  null=True)  # Field name made lowercase.
    contactinfo = models.CharField(db_column='ContactInfo', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    helpproblem = models.CharField(db_column='HelpProblem', max_length=200, blank=True,
                                   null=True)  # Field name made lowercase.
    imei = models.CharField(db_column='Imei', max_length=50, blank=True, null=True)  # Field name made lowercase.
    osversion = models.IntegerField(db_column='OsVersion', blank=True, null=True)  # Field name made lowercase.
    appversion = models.CharField(db_column='AppVersion', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=50, blank=True, null=True)  # Field name made lowercase.
    network = models.CharField(db_column='Network', max_length=50, blank=True, null=True)  # Field name made lowercase.
    reporttime = models.DateTimeField(db_column='ReportTime')  # Field name made lowercase.
    problemfrom = models.CharField(db_column='ProblemFrom', max_length=100)  # Field name made lowercase.
    problempath = models.TextField(db_column='ProblemPath', blank=True,
                                   null=True)  # Field name made lowercase. This field type is a guess.
    state = models.IntegerField(db_column='State')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserHelpLog'


class Userrequire(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=50)  # Field name made lowercase.
    requirement = models.CharField(db_column='Requirement', max_length=50)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserRequire'


class UserSurvival(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    imei = models.CharField(db_column='Imei', max_length=50)  # Field name made lowercase.
    firsttime = models.DateTimeField(db_column='FirstTime', blank=True, null=True)  # Field name made lowercase.
    lasttime = models.DateTimeField(db_column='LastTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'UserSurvival'

    def survival_day(self):
        return self.__survival(timedelta(days=1))

    def survival_week(self):
        return self.__survival(timedelta(weeks=1))

    def survival_month(self):
        return self.__survival(MonthDelta(months=1))

    def survival_year(self):
        return self.__survival(MonthDelta(months=12))

    def survival_last_week(self):
        from django.utils import timezone
        return self.lasttime + timedelta(weeks=1) > timezone.now()

    def __survival(self, delta):
        end_time = self.firsttime + delta;
        if end_time <= timezone.now():
            return self.lasttime > self.firsttime + delta
        else:
            return None


class AnalyzeRecord(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(db_column='action', max_length=50)
    time = models.DateTimeField(db_column='time', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'AnalyzeRecord'
