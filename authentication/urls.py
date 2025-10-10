# authentication/urls.py
from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('fetch_weight/', views.fetch_weight, name='fetch_weight'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('dashboard/', views.dashboard, name='home'),
    path('signup/', signup_view, name='signup'),
    path('weighing_process/', submit_weight, name='weighing_process'),
    path('export-weights/', export_weights, name='export_weights'),
    
    # Business Features
    path('chart_data/', views.chart_data, name='chart_data'),
    path('edit_record/<int:record_id>/', views.edit_record, name='edit_record'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('all-records/', views.all_records, name='all_records'),
]
