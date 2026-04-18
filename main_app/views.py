from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Report
from django.shortcuts import render

class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'
    
    def home(request):
        return render(request, 'home.html')

    def report_list(request):
        reports = Report.objects.all()
        return render(request, 'report_page.html', {'reports': reports})

# CREATE
class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan")  # ✅ ALERT
        return super().form_valid(form)


# UPDATE
class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate")  # ✅ ALERT
        return super().form_valid(form)


# DELETE
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus")  # ✅ ALERT
        return super().delete(request, *args, **kwargs)


# UPDATE STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.status = request.POST.get('status')
        report.save()

        messages.success(request, "Status berhasil diubah")  # ✅ ALERT

        return redirect('report_list')


# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

def home(request):
        return render(request, 'main_app/home.html')

def about(request):
    return render(request, 'about/about.html')

def contacts(request):
    return render(request, 'contacts/contacts.html')

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'main_app/report_detail.html', {'report': report})