from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from login.models import login
from summarize.models import Summary
from social_django.models import UserSocialAuth
from django.contrib.auth import logout
import json


def home(request):
	return render(request,'login/home.html')


def profile(request,url_id):
	user=request.user
	x=0
	if user.is_authenticated():
		if url_id.startswith('u'):
			x=1
		toi=request.POST.get('toi')
		ht=request.POST.get('ht')
		cnn=request.POST.get('cnn')
		response=render(request,'login/profile.html',{"x":x})
		if not login.objects.filter(email=user.email).exists():
			login.objects.create(name=user.get_full_name(),userid=user.username,email=user.email)
		if not request.COOKIES.has_key('tldr'):
			response.set_cookie('tldr', True)	
		return response
	return redirect('login')

def settings(request):
    return render(request, 'login/settings.html')

def users(request):
    x=login.objects.all()
    return render(request,'login/index.html',{"users":x})
def user_settings(request):
	nol=request.POST.get('nol')
	toi=request.POST.get('toi')
	ht=request.POST.get('ht')
	cnn=request.POST.get('cnn')
	user_email=request.user.email
	obj=login.objects.get(email=user_email)
	obj.nol=nol
	obj.toi=toi
	obj.cnn=cnn
	obj.ht=ht
	obj.save()
	return HttpResponse("Sucessfully added")
def before_settings(request):
	email=request.user.email
	user=login.objects.get(email=email)
	nol=user.nol
	toi=user.toi
	ht=user.ht
	cnn=user.cnn
	data=json.dumps([{"nol":nol,"toi":toi,"ht":ht,"cnn":cnn}])
	return HttpResponse(data,content_type="application/json")

def user_logout(request):
    logout(request)
    response = redirect('/')
    response.delete_cookie('tldr')
    return response