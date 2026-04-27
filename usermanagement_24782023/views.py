from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import RegisterForm

# ================= LOGIN =================
class CustomLoginView(LoginView):
    template_name = 'usermanagement/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Berhasil login")
        return super().form_valid(form)
    
    def get_success_url(self):
        if self.request.user.is_superuser:
            return '/admin/'
        return '/'


# ================= LOGOUT =================
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Berhasil logout")
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self):
        return reverse_lazy('login')


# ================= REGISTER =================
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_admin = False   # pastikan field ini ada di model
        user.save()
        messages.success(request, "Berhasil register")
        return redirect('login')

    return render(request, 'usermanagement/register.html', {'form': form})