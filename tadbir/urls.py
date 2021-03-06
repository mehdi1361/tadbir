"""tadbir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.conf import settings
from employee.views import dashboard, login
# from bank.views import BranchAutoComplete
from django.conf.urls.static import static
from reports.views import get_daily_user, get_g
from django.conf.urls import handler404, handler500
from bank import views as myapp_views
# from material.frontend import urls as frontend_urls

urlpatterns = [
    url(r'^$', dashboard, name='main'),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/login/', login, name='login'),
    url(r'^bank/', include('bank.urls', namespace='bank', app_name='bank')),
    url(r'^employee/', include('employee.urls', namespace='employee', app_name='employee')),
    url(r'^reports/', include('reports.urls', namespace='reports', app_name='reports')),
    url(r'^logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/', include('reports.urls', namespace='api', app_name='api')),
    url(r'^test/$', get_g, name='t'),
    url(r'^report_builder/', include('report_builder.urls'), name='report_builder'),
    # url(r'', include(frontend_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = myapp_views.error_404
handler500 = myapp_views.error_500