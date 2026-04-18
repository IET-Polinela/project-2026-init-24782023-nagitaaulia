from django.urls import path
from . import views
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    ReportDetailView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('reports/', ReportListView.as_view(), name='report_list'),

    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status'),
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('detail/<int:pk>/', views.report_detail, name='report_detail'),
]