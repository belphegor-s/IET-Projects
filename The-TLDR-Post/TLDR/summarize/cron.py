# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

import feedparser
from unidecode import unidecode
from .models import Summary, RSSlinks
from api.pyteaser_edit import SummarizeUrl1


def remove_non_ascii(text):
    return unidecode(text)


def scheduled_job():
    Summary.objects.all().delete()
    for e in RSSlinks.objects.all():
    	rss = e.rss_link
    	source = e.rss_title
    	count = e.number_of_feeds
        d = feedparser.parse(rss)
        l = len(d.entries)
        if l >= count:
            cnt = 1
            i = -1
            while (cnt <= count):
                i += 1
                if i >= l:
                    break
                foo = []
                post = d.entries[i]
                url = post.link
                try:
                    summary = SummarizeUrl1(url, 5)
                    if summary is not None:
                        for x in summary:
                            foo.append(remove_non_ascii(x))
                    summary_url = ' '.join(foo)
                except AttributeError as e:
                    continue
                try:
                    title = post.title
                except AttributeError as e:
                    continue
                if len(foo) is 5 and summary_url is not None:
                    data = Summary(title=title, url=url, summarize_url=summary_url, source=source)
                    data.save()
                    cnt += 1
