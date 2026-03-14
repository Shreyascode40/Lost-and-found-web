from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Institution
from items.models import Item
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from accounts.models import CustomUser


def institution_detail(request, slug):
    institution = get_object_or_404(Institution, slug=slug)

    items = Item.objects.filter(
        institution=institution,
        item_type='Lost',
        is_active=True
    )

    return render(request, "institution/detail.html", {
        "institution": institution,
        "items": items
    })


def admin_register(request):
    if request.user.is_authenticated and request.user.is_institution_admin:
        return redirect("admin_panel:admin_dashboard")
    
    if request.method == "POST":
        institution_name = request.POST.get("institution_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            return render(request, "admin_panel/admin_register.html", {
                "error": "Passwords do not match"
            })
        
        if CustomUser.objects.filter(username=username).exists():
            return render(request, "admin_panel/admin_register.html", {
                "error": "Username already exists"
            })
        
        institution = Institution.objects.create(
            name=institution_name,
            slug=institution_name.lower().replace(" ", "-"),
            join_password=password
        )
        
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            institution=institution,
            is_institution_admin=True
        )
        
        return redirect("admin_panel:admin_login")
    
    return render(request, "admin_panel/admin_register.html")