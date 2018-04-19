from rest_framework import serializers
from summarize.models import Summary

class SummarySerializer(serializers.ModelSerializer):
	class Meta:
		model = Summary
		fields = [
			'title',
			'url',
			'summarize_url',
			'source',
		]
