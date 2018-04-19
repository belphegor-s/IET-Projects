# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    )
import re
import json
import urllib2
from summarize.models import Summary
from .serializers import SummarySerializer
from django.http import Http404, HttpResponse, JsonResponse
from django.utils.encoding import smart_str, smart_unicode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pyteaser import SummarizeUrl
from django.utils.safestring import mark_safe
from lxml.html import parse
from ast import literal_eval
from unidecode import unidecode
from .pyteaser_edit import SummarizeUrl1
from login.models import login

def remove_non_ascii(text):
    return unidecode(text)

class SummaryAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        queryset = Summary.objects.all()
        serializer = SummarySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        url = request.data.get('url')
        source = request.data.get('source')
        s = SummarizeUrl(url)
        foo = []
        for x in s:
            foo.append(remove_non_ascii(x))    
        summary = ' '.join(foo) 
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
        data = {'title': title, 'url': url, 'summarize_url': summary, 'source': source}
        serializer = SummarySerializer(data=data)
        if serializer.is_valid():
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):    
        data = []
        for e in Summary.objects.all():
            if request.user.is_authenticated():
                email = request.user.email
                user = login.objects.get(email=email)
                i = user.nol
                src = e.source 
                flag =0  
                if user.toi is True and src.encode('utf8') == 'Times of India' and flag != 2:
                    source = 'Times of India'
                    flag += 1
                elif user.cnn is True and src.encode('utf8') == 'CNN' and flag != 2:
                    source = 'CNN'
                    flag += 1
                elif user.ht is True and src.encode('utf8') == 'Hindustan Times' and flag != 2:
                    source = 'Hindustan Times' 
                    flag += 1
                else: 
                    source = None          
                s = SummarizeUrl1(e.url, i)
                foo = []
                for x in s:
                    foo.append(remove_non_ascii(x))         
                x = ' '.join(foo)
                if len(s) is i and source is not None:
                    data.append({'title': e.title, 'url': e.url, 'summarize_url': x, 'source': source})  
            
        if not len(data):
            queryset = Summary.objects.all()
            serializer = SummarySerializer(queryset, many=True)
            return Response(serializer.data)     
        json_data = json.dumps(data)                      
        return HttpResponse(json_data, content_type="application/json") 



    def post(self, request, format=None):
        nol = request.data.get('nol')
        ht = request.data.get('ht')
        cnn = request.data.get('cnn')
        toi = request.data.get('toi')
        data = []
        for e in Summary.objects.all():
            src = e.source 
            flag =0
            foo = []  
            if toi is True and src.encode('utf8') == 'Times of India' and flag != 2:
                source = 'Times of India'
                flag += 1
            elif cnn is True and src.encode('utf8') == 'CNN' and flag != 2:
                source = 'CNN'
                flag += 1
            elif ht is True and src.encode('utf8') == 'Hindustan Times' and flag != 2:
                source = 'Hindustan Times' 
                flag += 1
            else: 
                source = None         
            s = SummarizeUrl1(e.url, nol)
            for x in s:
                foo.append(remove_non_ascii(x))    
            x = ' '.join(foo)
            if source is not None:
                data.append({'title': e.title, 'url': e.url, 'summarize_url': x, 'source': source})  
        if not len(data):
            queryset = Summary.objects.all()
            serializer = SummarySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)       
        serializer = SummarySerializer(data=data, many=True) 
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


                