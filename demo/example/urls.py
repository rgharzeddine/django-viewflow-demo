from viewflow.flow.viewset import FlowViewSet

from django.conf.urls import url, include

from . import views
from .flows import DailyTimesheetApprovalFlow, VacationApprovalFlow

sheet_urls = FlowViewSet(DailyTimesheetApprovalFlow).urls
vacation_urls = FlowViewSet(VacationApprovalFlow).urls

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^fast_login$', views.fast_login, name='fast_login'),
    url(r'^fast_logout$', views.fast_logout, name='fast_logout'),
    url(r'^timesheet$', views.DailyTimesheetListView.as_view(),
        name='timesheets'),
    url(r'^vacation$', views.VacationListView.as_view(),
        name='vacations'),

    url(r'^task/completed/$', views.CompletedTaskListView.as_view(),
        name='tasks_completed'),

    url(r'^task/in_progress/$', views.InProgressTaskListView.as_view(),
        name='tasks_in_progress'),

    url(r'^task/unassigned/$', views.UnassignedTaskListView.as_view(),
        name='tasks_unassigned'),

    url(r'^process$', views.ProcessListView.as_view(),
        name='processes'),
    url(r'^process_classes$', views.ProcessClassesListView.as_view(),
        name='process_classes'),

    url(r'^daily/', include(sheet_urls, namespace='daily')),
    url(r'^vacation/', include(vacation_urls, namespace='vacation')),

]
