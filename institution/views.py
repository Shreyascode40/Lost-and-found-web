from django.shortcuts import render, get_object_or_404
from .models import Institution
from items.models import Item

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