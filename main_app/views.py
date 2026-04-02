from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm

def add_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'main_app/add_report.html', {'form': form})

def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})

def update_report(request, id):
    report = get_object_or_404(Report, id=id)
    form = ReportForm(request.POST or None, instance=report)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'main_app/add_report.html', {'form': form})

def delete_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.delete()
    return redirect('home')

def verify_report(request, id):
    report = get_object_or_404(Report, id=id)
    report.status = 'VERIFIED'
    report.save()
    return redirect('home')