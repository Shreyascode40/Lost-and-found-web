from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from claim.models import Claim
from items.models import Item



@login_required
def claim_list(request):
    claims = Claim.objects.filter(claimant=request.user).order_by('-created_at')
    return render(request, "claim/claim_list.html", {
        "claims": claims
    })

@login_required
def create_claim(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    #  SECURITY CHECKS

    #  Cannot claim your own item
    if item.user == request.user:
        messages.error(request, "You cannot claim your own item.")
        return redirect('home')

    # Cannot claim from another institution
    if item.institution != request.user.institution:
        return HttpResponseForbidden("Access Denied")

    #  Cannot claim inactive item
    if not item.is_active:
        messages.warning(request, "This item is already closed.")
        return redirect('items:home')

    #  Cannot claim twice
    if Claim.objects.filter(item=item, claimant=request.user).exists():
        messages.warning(request, "You have already submitted a claim.")
        return redirect('items:home')

    if request.method == "POST":
        message = request.POST.get('message')

        if not message:
            messages.error(request, "Please enter a message.")
            return redirect('create_claim', item_id=item.id)

        Claim.objects.create(
            item=item,
            claimant=request.user,
            message=message
        )

        messages.success(request, "Claim request sent successfully!")
        return redirect('items:home')

    return render(request, "claim/create_claim.html", {
        "item": item
    })



@login_required
def owner_claims(request):

    claims = Claim.objects.filter(item__user=request.user).order_by('-created_at')

    return render(request, "claim/owner_claims.html", {
        "claims": claims
    })



@login_required
def accept_claim(request, claim_id):

    if request.method != "POST":
        return HttpResponseForbidden()

    claim = get_object_or_404(Claim, id=claim_id)

    #  Check if user is institution admin
    if not request.user.is_institution_admin:
        return HttpResponseForbidden("Access Denied")

    #  Check if same institution
    if claim.item.institution != request.user.institution:
        return HttpResponseForbidden("Wrong Institution")

    # Update claim status
    claim.status = "Accepted"
    claim.save()

    # Close item
    claim.item.is_active = False
    claim.item.save()

    # Reject other claims automatically
    Claim.objects.filter(
        item=claim.item
    ).exclude(id=claim.id).update(status="Rejected")

    messages.success(request, "Claim accepted and item handed over successfully.")

    return redirect('admin_dashboard')




@login_required
def reject_claim(request, claim_id):
    claim = get_object_or_404(Claim, id=claim_id)

    #  Only owner can reject
    if claim.item.user != request.user:
        return HttpResponseForbidden("Access Denied")

    claim.status = "Rejected"
    claim.save()

    messages.info(request, "Claim rejected.")

    return redirect('owner_claims')
