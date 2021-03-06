"""foodcalc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from calcs import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/([0-9]+)$', views.event, name='show-event'),
    url(r'^events/create$', views.create_event, name='create-event'),
    url(r'^mealcost/([0-9]+)$', views.mealcost, name='cost-breakdown'),
	url(r'^ingredients/([0-9]+)/inevent/([0-9]+)$', views.ingredient, name='ingredient'),
    url(r'', views.show_events),
]
