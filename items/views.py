from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def home(request):

    items = Item.objects.filter(
        institution=request.user.institution,
        item_type='Lost',
        is_active=True
    ).order_by('-created_at')

    return render(request, "home.html", {
        "items": items
    })

@login_required

def add_item(request):
    if request.method == "POST":
        item = Item.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            item_type=request.POST.get('item_type'),
            user=request.user,
            institution=request.user.institution
        )
        return redirect('home')
    


def lost_items(request):

    items = Item.objects.filter(item_type='Lost').order_by('-id')
    return render(request, 'lost_items.html', {'items': items})


@login_required
def item_detail(request, item_id):

    item = Item.objects.get(id=item_id)

    return render(request, "item_detail.html", {

        "item": item

    })
