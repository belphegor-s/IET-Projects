# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Summary, RSSlinks

# Register your models here.

class SummaryAdmin(admin.ModelAdmin):
	list_display = ["url","source"]
	class Meta:
		model = Summary

admin.site.register(Summary, SummaryAdmin)

class RSSlinksAdmin(admin.ModelAdmin):
	list_display = ["rss_link","rss_title"]
	class Meta:
		model = RSSlinks

admin.site.register(RSSlinks, RSSlinksAdmin)
