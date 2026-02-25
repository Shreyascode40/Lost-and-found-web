from django.urls import path
from . import views


app_name = "admin_panel"

urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
