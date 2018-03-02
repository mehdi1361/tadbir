import jdatetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart, PivotDataPool
from .models import PersonDailyReport
from django.http import JsonResponse
from django.db.models import Q, Sum


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


def get_daily_user(request, *args, **kwargs):
    today = jdatetime.datetime.now()
    day = today + jdatetime.timedelta(-30)
    reports = PersonDailyReport.objects.filter(
        Q(persian_date__lte=today), Q(persian_date__gte=day),
        user=request.user
    )
    labels = []
    default_items = []

    for report in reports:
        labels.append(str(report.persian_date))
        default_items.append(report.count_file_daily)

    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)  # http response


def get_daily_file_user(request, *args, **kwargs):
    today = jdatetime.datetime.now()
    day = today + jdatetime.timedelta(-30)
    reports = PersonDailyReport.objects.filter(
        Q(persian_date__lte=today), Q(persian_date__gte=day),
        user=request.user
    )
    labels = []
    default_items = []

    for report in reports:
        labels.append(str(report.persian_date))
        default_items.append(report.value_file_daily)

    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)  # http response


def get_g(request):
    return render(request, 'bank/employee/chart.html', {"customers": 10})


@login_required(login_url='/employee/login/')
def get_users_reports(request):
    # TODO complete report from request persian calendar
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    if start_date and end_date:
        employee_report = PersonDailyReport.objects.values('user') \
            .filter(Q(persian_date__lte=end_date), Q(persian_date__gte=start_date)) \
            .annotate(
                sum_count_file=Sum('count_file'),
                sum_value_file=Sum('value_file'),
                sum_count_daily=Sum('count_file_daily'),
                sum_value_file_daily=Sum('value_file_daily'),
                sum_count_file_recovery=Sum('count_file_recovery'),
                sum_value_file_recovery=Sum('value_file_recovery')
            )

    else:
        employee_report = PersonDailyReport.objects.values('user') \
            .annotate(
                sum_count_file=Sum('count_file'),
                sum_value_file=Sum('value_file'),
                sum_count_daily=Sum('count_file_daily'),
                sum_value_file_daily=Sum('value_file_daily'),
                sum_count_file_recovery=Sum('count_file_recovery'),
                sum_value_file_recovery=Sum('value_file_recovery')
            )

    return render(request, 'bank/reports/list.html', {'report': employee_report})
