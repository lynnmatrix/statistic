from django.contrib import admin

# Register your models here.
from statistic.models import Domainconfig, Activedevicelog


@admin.register(Domainconfig)
class DomainconfigAdmin(admin.ModelAdmin):
	list_display = ('domain',)


@admin.register(Activedevicelog)
class DateFilterAdmin(admin.ModelAdmin):
	list_filter = ['time', 'umengchannel']
	list_display = ('imei', 'time')