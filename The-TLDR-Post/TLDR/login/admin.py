from django.contrib import admin

# Register your models here.
from .models import login

class loginAdmin(admin.ModelAdmin):
	list_display = ["name","email"]
	class Meta:
		model = login


admin.site.register(login, loginAdmin)