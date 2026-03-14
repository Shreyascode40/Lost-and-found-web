from django.urls import path
from . import views

app_name = 'institution'

urlpatterns = [
    path('register/', views.admin_register, name='admin_register'),
    path('<slug:slug>/', views.institution_detail, name='institution_detail'),
]
