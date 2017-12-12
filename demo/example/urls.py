from viewflow.flow.viewset import FlowViewSet

from django.conf.urls import url, include
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.decorators import login_required
# from django.views.generic import TemplateView

from . import views

from .flows import DailyTimesheetApprovalFlow
sheet_urls = FlowViewSet(DailyTimesheetApprovalFlow).urls


urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^fast_login$', views.fast_login, name='fast_login'),
    url(r'^fast_logout$', views.fast_logout, name='fast_logout'),
    url(r'^timesheet$', views.DailyTimesheetListView.as_view(),
        name='timesheets'),

    url(r'^task$', views.TaskListView.as_view(),
        name='tasks'),
    url(r'^process$', views.ProcessListView.as_view(),
        name='processes'),

    url(r'^daily/', include(sheet_urls, namespace='wf')),

]
