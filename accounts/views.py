from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.hashers import check_password
from institution.models import Institution
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import CustomUser

# Create your views here.


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

        institution = Institution.objects.get(id=institution_id)

        #  Check institution join password
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
            return redirect('items:home')  # Make sure this exists in urls
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid Credentials'
            })

    return render(request, 'accounts/login.html')


def admin_login(request):

    #  If admin already logged in → redirect to dashboard
    if request.user.is_authenticated and request.user.is_institution_admin:
        return redirect("admin_dashboard")


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        #  Check if user exists
        if user is not None:

            #  Check if user is admin
            if user.is_institution_admin:

                login(request, user)

                return redirect("admin_dashboard")

            else:
                messages.error(request,
                            "You are not authorized as admin.")

        else:
            messages.error(request,
                        "Invalid username or password.")


    return render(request,
                "admin_panel/admin_login.html")


    


@login_required
def admin_logout(request):
    logout(request)
    return redirect("login")



@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")