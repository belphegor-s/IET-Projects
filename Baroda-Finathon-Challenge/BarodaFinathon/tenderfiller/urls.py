from django.conf.urls import url
from django.contrib import admin

from .views import (
	TenderFillingAPI,
	)

urlpatterns = [
	url(r'^$', TenderFillingAPI.as_view(), name='nestoria')
]