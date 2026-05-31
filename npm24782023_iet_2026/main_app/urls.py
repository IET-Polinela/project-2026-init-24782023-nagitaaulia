from django.urls import path
from . import views
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    ReportDetailView,
    report_detail_json,
    home,
    about,
    contacts
)

urlpatterns = [
    path('', home, name='home'),

    # LIST
    path('reports/', ReportListView.as_view(), name='report_list'),
    path('search/', views.live_search, name='live_search'),

    # CRUD
    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),

    # STATUS
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status'),

    # DETAIL (PAKAI SATU SAJA)
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('detail-json/<int:pk>/', report_detail_json, name='report_detail_json'),

    # STATIC PAGE
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
]