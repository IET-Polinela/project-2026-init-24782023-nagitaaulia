from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Report


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak!")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

# LIST (READ)
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login dulu!")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Report.objects.all().order_by('-id')


# DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Silakan login dulu!")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


# CREATE
class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)



# UPDATE
class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate")
        return super().form_valid(form)



# DELETE
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Laporan berhasil dihapus")
        return super().delete(request, *args, **kwargs)



# UPDATE STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, "Akses Ditolak!")
            return redirect('report_list')

        report = get_object_or_404(Report, pk=pk)
        report.status = request.POST.get('status')
        report.save()

        messages.success(request, "Status berhasil diubah")
        return redirect('report_list')
    
# ======================
# STATIC PAGES
# ======================

def home(request):
    return render(request, 'main_app/home.html')

def about(request):
    return render(request, 'about/about.html')

def contacts(request):
    return render(request, 'contacts/contacts.html')