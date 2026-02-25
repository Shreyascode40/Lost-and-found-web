from django.contrib import admin
from django.urls import path
from django.urls import include 
from . import views

app_name = 'accounts'




urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/', views.logout_view, name='logout')
]