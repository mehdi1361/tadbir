from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart, PivotDataPool
from .models import PersonDailyReport


def weather_chart_view(request):
    weatherdata = DataPool(
           series=
            [{'options': {
               'source': PersonDailyReport.objects.all()},
              'terms': [
                'id',
                'count_file_daily',
                'count_file_recovery']}
             ])

    cht = Chart(
            datasource=weatherdata,
            series_options=[{'options': {
                  'type': 'line',
                  'stacking': False},
                'terms': {
                  'id': [
                    'count_file_daily',
                    'count_file_recovery']
                  }}],
            chart_options={'title': {
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})

    return render_to_response('bank/reports/test.html', {'weatherchart': cht})

