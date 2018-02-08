from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^list/$', views.files, name='list'),
    url(r'^profile/$', views.register_profile, name='profile'),
    url(r'^files/detail/(?P<file_id>\d+)$', views.file_document, name='employee_file_detail'),
]
