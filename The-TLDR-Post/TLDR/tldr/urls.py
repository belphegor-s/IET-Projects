"""tldr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from login import views as core_views
from summarize import views

urlpatterns = [
    # url(r'^$',core_views.home,name='home'),
    url(r'^admin/', admin.site.urls),
    # API Urls
    url(r'^$', views.summary, name='summary'),
    url(r'^api/summary/', include("summarize.api.urls", namespace='summarize-api')),
    # url(r'^feeds/', include("feeds.urls", namespace='feeds-api')),
    # url(r'^thanks/$', views.thanks, name='thanks'),
    # OAuth Urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', core_views.user_logout, name='logout'),
    # url(r'^logout/$', auth_views.logout, name='logout',kwargs={'next_page': '/'}),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^profile/(?P<url_id>[a-z]*)',core_views.profile,name="profile"), 
    url(r'^settings/', core_views.settings, name='settings'),
    url(r'^users/', core_views.users, name='users'),
    url(r'^ajax/settings/',core_views.user_settings,name='user_settings'),
    url(r'^ajax/before/',core_views.before_settings,name="before_settings"),
    # Web
    # url(r'^web/',views.)
]

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = '/login/'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
