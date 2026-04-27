from django.urls import path
from .views import (
    ReportListView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    ReportDetailView,
    home,
    about,
    contacts
)

urlpatterns = [
    path('', home, name='home'),

    # LIST
    path('reports/', ReportListView.as_view(), name='report_list'),

    # CRUD
    path('add/', ReportCreateView.as_view(), name='report_add'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='report_edit'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='report_delete'),

    # STATUS
    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='report_status'),

    # DETAIL (PAKAI SATU SAJA)
    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    # STATIC PAGE
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
]