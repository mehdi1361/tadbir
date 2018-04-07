from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^list/$', views.files, name='list'),
    url(r'^profile/$', views.register_profile, name='profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^files/detail/(?P<file_id>\d+)$', views.file_document, name='employee_file_detail'),
    url(r'^employee/auth/(?P<id>\d+)$', views.edit_auth_employee_file, name='auth_edit'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
    url(r'^manage/$', views.create_employee, name='manage'),
    url(r'^employee_manage/(?P<emp_id>\d+)$', views.employee_permission_view, name='permission'),
    url(r'^manage_edit/(?P<permission_id>\d+)$', views.edit_employee_permission, name='edit_permission'),

]
