from django.contrib import admin

# Register your models here.
from statistic.models import Domainconfig


@admin.register(Domainconfig)
class DomainconfigAdmin(admin.ModelAdmin):
	pass
