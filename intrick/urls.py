"""intrick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin

from blog import views

urlpatterns = [
    url(r'^redactor/', include('redactor.urls')),
    url(r'^blogs/(?P<slug>[-\w]+)/(?P<blog_id>\d+)/$', views.blog_view, name='blog_view'),
    url(r'^subscribe-newsletter$', views.subscribe_newsletter, name='subscribe_newsletter'),
    url(r'^blogs/$', views.bloglist_view, name='bloglist_view'),
    url(r'^$', views.home_view, name='home_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    url(r'get-message/', views.get_message_from_viewer, name='get_message')
]
