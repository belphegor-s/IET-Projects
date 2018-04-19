from django.conf.urls import url
from django.contrib import admin

from .views import (
	BranchEvaluationAPI,
	)

urlpatterns = [
	url(r'^$', BranchEvaluationAPI.as_view(), name='branch_evaluation')
]