# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

import urllib2
from lxml.html import parse

from django.shortcuts import render

from django.http import HttpResponse

from django.http import JsonResponse

from .models import Summary
from pyteaser import SummarizeUrl
from .forms import SummaryForm
# Create your views here.
def summary(request):
	title = 'Summary'
	form = SummaryForm(request.POST or None)
	response_data = {}
	context = {
		"title": title,
		"form": form,
	}
	if request.method == 'POST':		
		instance = form.save(commit=False)
		url = instance.url
		if form.is_valid():
			summary = SummarizeUrl(url)
			instance.summarize_url = summary
			hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
			       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			       'Accept-Encoding': 'none',
			       'Accept-Language': 'en-US,en;q=0.8',
			       'Connection': 'keep-alive'
			       }     
			req = urllib2.Request(url, headers=hdr)
			page = urllib2.urlopen(req)
			p = parse(page)
			title = p.find(".//title").text
			instance.title = title
			# instance.save()
			response_data['url'] = instance.url
			response_data['title'] = title
			response_data['summary'] = instance.summarize_url 
			context = {
				"title": title,
				"url": url,
				"summary": summary,
			}
			return JsonResponse(response_data)
		else:
			return JsonResponse({"nothing to see": "this isn't happening"})
			
	else:
		form = SummaryForm()		
	


	return render(request, "website/index.html", context)



