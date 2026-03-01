from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item

@login_required
def home(request):
    if not request.user.institution:
        messages.error(request, "Please select an institution in your profile.")
        return render(request, "home.html", {"items": []})
    
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
    if not request.user.institution:
        messages.error(request, "Please select an institution in your profile.")
        return redirect('items:home')
    
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        item_type = request.POST.get('item_type')
        location = request.POST.get('location')
        date = request.POST.get('date')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        item = Item.objects.create(
            title=title,
            description=description,
            item_type=item_type,
            location=location,
            date=date,
            category=category,
            image=image,
            user=request.user,
            institution=request.user.institution
        )
        messages.success(request, f'{item_type} item "{title}" has been added successfully!')
        return redirect('home')
    
    return render(request, "add_item.html")

@login_required
def lost_items(request):
    if not request.user.institution:
        items = Item.objects.none()
    else:
        items = Item.objects.filter(
            institution=request.user.institution,
            item_type='Lost'
        ).order_by('-id')
    return render(request, 'lost_items.html', {'items': items})


@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "item_detail.html", {
        "item": item
    })
