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
    url(r'^branch/edit/(?P<branch_id>\d+)$', views.edit_branch, name='edit_branch'),
    url(r'^files/$', views.file_list, name='files_list'),
    url(r'^files/new/$', views.new_file, name='new_file'),
    url(r'^files/detail/(?P<file_id>\d+)$', views.file_document, name='file_detail'),
    url(r'^api/get_branches/', views.get_branch, name='get_branches'),
    url(r'^files/new_person/$', views.new_person, name='new_person'),
    url(r'^persons/list/$', views.get_persons, name='get_persons'),
    url(r'^lawyers/list/$', views.get_lawyers, name='get_lawyers'),
    url(r'^lawyers/new/$', views.new_lawyer, name='new_lawyer'),
    url(r'^follow/law/$', views.follow_law, name='follow_in_law'),
    url(r'^files/new_person_office/$', views.new_person_office, name='new_person_office'),
    url(r'^persons_office/list/$', views.get_person_office, name='persons_office'),
    url(r'^sms_type/$', views.sms_type_list, name='sms_type'),
    url(r'^files/detail/person_edit/(?P<person_id>\d+)$', views.edit_person_detail, name='file_detail_person_edit'),
]
