from django.urls import path
from .views import CustomLoginView, CustomLogoutView
from . import views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
]