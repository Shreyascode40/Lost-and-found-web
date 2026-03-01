from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from institution.models import Institution
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        institution_id = request.POST.get("institution")
        join_password = request.POST.get("join_password")

        if password != confirm_password:
            return render(request, "accounts/register.html", {
                "error": "Passwords do not match"
            })

        if not institution_id:
            return render(request, "accounts/register.html", {
                "error": "Please select an institution"
            })

        try:
            institution = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            return render(request, "accounts/register.html", {
                "error": "Invalid institution selected"
            })

        if not check_password(join_password, institution.join_password):
            return render(request, "accounts/register.html", {
                "error": "Invalid Institution Password"
            })

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            institution=institution,
        )

        return redirect("accounts:login")

    institutions = Institution.objects.all()

    return render(request, "accounts/register.html", {
        "institutions": institutions
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('items:home')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


def admin_login(request):
    if request.user.is_authenticated and request.user.is_institution_admin:
        return redirect("admin_panel:admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_institution_admin:
            login(request, user)
            return redirect("admin_panel:admin_dashboard")
        else:
            return render(request, "admin_panel/admin_login.html", {
                "error": "Invalid admin credentials"
            })

    return render(request, "admin_panel/admin_login.html")


@login_required
def admin_logout(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")