# authentication/urls.py
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='home'),
    path('signup/', signup_view, name='signup'),
    # path('weighing_process/', views.weighing_process, name='weighing_process'),
    path('weighing_process/', submit_weight, name='weighing_process'),
    # path('submit-weight/', submit_weight, name='submit_weight'),
    path('export-weights/', export_weights, name='export_weights'),
]
