from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^list/$', views.files, name='list'),
]
