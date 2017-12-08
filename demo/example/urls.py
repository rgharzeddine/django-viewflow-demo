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
    # url(r'^timesheet/add$', views.DailyTimesheetCreateView.as_view(),
    #     name='add_daily'),
    # url(r'^timesheet/(?P<pk>\d+)/$', views.DailyTimesheetUpdateView.as_view(),
    #     name='update_daily'),
    url(r'^timesheet$', views.DailyTimesheetListView.as_view(),
        name='timesheets'),

    url(r'^task$', views.TaskListView.as_view(),
        name='tasks'),

    url(r'^daily/', include(sheet_urls, namespace='wf')),

    # url(r'^daily/start/',
    #     views.CreateDailyTimesheetView.as_view(),
    #     dict(
    #         flow_class=DailyTimesheetApprovalFlow,
    #         flow_task=DailyTimesheetApprovalFlow.start,
    #     ),
    #     name='start_daily'),

    # url(r'^daily/approve/',
    #     views.ApproveDailyTimesheetView.as_view(),
    #     dict(
    #         flow_class=DailyTimesheetApprovalFlow,
    #         flow_task=DailyTimesheetApprovalFlow.approve,
    #     ),
    #     name='approve_daily'),

]
