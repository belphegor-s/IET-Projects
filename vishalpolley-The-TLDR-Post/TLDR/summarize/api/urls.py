from django.conf.urls import url
from django.contrib import admin

from .views import (
	SummaryAPIView,
	FeedsAPIView,
	)

urlpatterns = [
	url(r'^$', SummaryAPIView.as_view(), name='create'),
	url(r'^list/$', FeedsAPIView.as_view(), name='list'),
]
