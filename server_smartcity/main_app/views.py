from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Report
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Report.objects.values_list('category', flat=True).distinct()
        return context


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
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        messages.success(self.request, "Laporan berhasil ditambahkan")
        return super().form_valid(form)



# UPDATE
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/report_form.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if report.reporter != request.user:
            messages.error(request, "Anda hanya bisa mengedit laporan sendiri!")
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diupdate")
        return super().form_valid(form)



# DELETE
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()

        if (
            report.reporter != request.user
            and not request.user.is_staff
        ):
            messages.error(
                request,
                "Anda hanya bisa menghapus laporan sendiri!"
            )
            return redirect('report_list')

        return super().dispatch(request, *args, **kwargs)


# UPDATE STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
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

def live_search(request):
    query = request.GET.get('q', '').strip()

    reports = Report.objects.all()

    if query:
        reports = reports.filter(
            Q(category__icontains=query)
        )

    data = []
    for r in reports:
        data.append({
            'id': r.id,
            'title': r.title,
            'category': r.category,
            'location': r.location,
            'status': r.status,
        })

    return JsonResponse(data, safe=False)

def report_detail_json(request, pk):
    report = get_object_or_404(Report, pk=pk)

    data = {
        'id': report.id,
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }

    return JsonResponse(data)