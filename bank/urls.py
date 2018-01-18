from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.bank_list, name='bank_list'),
    url(r'^new/$', views.new_bank, name='new_bank'),
    url(r'^edit/(?P<bank_id>\d+)$', views.edit_bank, name='edit_bank'),
    url(r'^areas/$', views.management_area_list, name='areas_list'),
    url(r'^areas/new/$', views.new_area, name='new_area'),
    url(r'^areas/edit/(?P<area_id>\d+)$', views.edit_area, name='edit_area'),
    url(r'^branches/$', views.BranchListView.as_view(), name='branches_list'),
    # url(r'^branches/edit$', views.BranchListView.as_view(), name='edit_branch'),
    url(r'^branch/new/$', views.new_branch, name='new_branch'),
    url(r'^files/$', views.file_list, name='files_list'),
    url(r'^files/new/$', views.new_file, name='new_file'),
    url(r'^api/get_branches/', views.get_branch, name='get_branches'),
]
