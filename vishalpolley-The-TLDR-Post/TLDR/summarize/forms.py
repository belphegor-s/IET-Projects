from django import forms

from .models import Summary

class SummaryForm(forms.ModelForm):
	class Meta:
		model = Summary
		fields = ['url']
		widgets = {
            'url': forms.TextInput(attrs={
            	'id': 'search',
	            'placeholder': 'Type a url to summarize article'
            	}),
        }

	def __init__(self, *args, **kwargs): 
	    super(SummaryForm, self).__init__(*args, **kwargs)
	    self.fields['url'].label = ''    


	def clean_url(self):
		cleaned_data = super(SummaryForm, self).clean()
		url = cleaned_data.get('url')
		return url	