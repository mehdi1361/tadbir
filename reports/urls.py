from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^chart/$', views.weather_chart_view, name='new_bank'),
]