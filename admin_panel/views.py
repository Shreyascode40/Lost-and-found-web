from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item
from claim.models import Claim
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


@login_required
def admin_dashboard(request):
    if not request.user.is_institution_admin:
        return redirect("admin_panel:admin_login")

    institution = request.user.institution

    total_lost = Item.objects.filter(
        institution=institution,
        item_type='Lost'
    ).count()

    total_found = Item.objects.filter(
        institution=institution,
        item_type='Found'
    ).count()

    pending_claims = Claim.objects.filter(
        item__institution=institution,
        status='Pending'
    ).count()

    resolved_claims = Claim.objects.filter(
        item__institution=institution,
        status='Accepted'
    ).count()

    claims = Claim.objects.filter(
        item__institution=institution,
        status='Pending'
    ).order_by('-created_at')[:5]

    return render(request,
                "admin_panel/admin_dashboard.html",
                {
                    "total_lost": total_lost,
                    "total_found": total_found,
                    "pending_claims": pending_claims,
                    "resolved_claims": resolved_claims,
                    "claims": claims
                })


def admin_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,
                            username=username,
                            password=password)

        if user and user.is_institution_admin:

            login(request, user)

            return redirect("admin_panel:admin_dashboard")

        return render(request,
                    "admin_panel/admin_login.html",
                    {"error": "Invalid admin credentials"})

    return render(request,
                "admin_panel/admin_login.html")
