from django.conf.urls import url
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.decorators import login_required
# from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^fast_login$', views.fast_login, name='fast_login'),
    url(r'^fast_logout$', views.fast_logout, name='fast_logout'),
    url(r'^timesheet/add$', views.DailyTimesheetCreateView.as_view(),
        name='add_daily'),
    url(r'^timesheet/(?P<pk>\d+)/$', views.DailyTimesheetUpdateView.as_view(),
        name='update_daily'),
    url(r'^timesheet$', views.DailyTimesheetListView.as_view(),
        name='timesheets'),
]
