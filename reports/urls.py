from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^chart/$', views.weather_chart_view, name='new_bank'),
    url(r'^user/daily/$', views.get_daily_user, name='api-data'),
    url(r'^user/daily/value/$', views.get_daily_file_user, name='api-data-value'),
    url(r'^employee/$', views.get_users_reports, name='user-report'),
]