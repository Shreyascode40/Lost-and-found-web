from django.urls import path
from . import views

app_name = "items"


urlpatterns = [
    path('', views.home, name='home'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('add/', views.add_item, name='add_item'),
    path('lost/', views.lost_items, name='lost_items'),
]
