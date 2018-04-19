from django.conf.urls import url
from django.contrib import admin

from .views import (
	PersonalRecommendationAPI,
	)

urlpatterns = [
	url(r'^$', PersonalRecommendationAPI.as_view(), name='personal-recommendation')
]