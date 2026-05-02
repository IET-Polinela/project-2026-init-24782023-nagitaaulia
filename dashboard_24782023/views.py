from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'


def dashboard_data(request):
    status_data = Report.objects.values('status').annotate(total=Count('id'))
    category_data = Report.objects.values('category').annotate(total=Count('id'))

    latest_reported = Report.objects.filter(status='REPORTED').order_by('-id')[:5]
    latest_resolved = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

    return JsonResponse({
        'status': list(status_data),
        'category': list(category_data),
        'latest_reported': list(latest_reported.values()),
        'latest_resolved': list(latest_resolved.values()),
    })


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
