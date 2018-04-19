# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Summary(models.Model):
	title = models.TextField(default='', null=True)
	url = models.URLField(max_length=200, blank=False, null=False)
	summarize_url = models.TextField(default='', null=True)
	source = models.TextField(default='', null=True)

	def __str__(self):
		return self.url

class RSSlinks(models.Model):
	rss_link = models.URLField(max_length=200, blank=False, null=False)
	rss_title = models.TextField(default='', null=True)
	number_of_feeds = models.PositiveIntegerField(default=3)

	class Meta:
		verbose_name = 'RSS link'
		verbose_name_plural = 'RSS links'

	def __str__(self):
		return self.rss_title