"""rcon_ark_server URL Configuration

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
from django.conf.urls import url, patterns

urlpatterns = patterns('server.views',
                       url(r'command/', 'execute_command'),
                       url(r"login/", 'login'),
                       url(r"backgrounds/", "backgrounds"),

                       url(r"myservers/change/", "change_myservers"),
                       url(r"myservers/connect/", "connect_to_server"),
                       url(r"myservers/delete/", "delete_server"),
                       url(r"myservers/", "get_myservers"),

                       url(r"items/", "get_items")
                       )
