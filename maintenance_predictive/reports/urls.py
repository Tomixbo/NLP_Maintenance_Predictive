from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.list_reports, name='list_reports'),
    path('new/', views.create_report, name='create_report'),
    path('detail/<int:pk>/', views.report_detail, name='report_detail'),
]
