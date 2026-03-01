from django.urls import path
from . import views


app_name = 'claim'


urlpatterns = [
    path('list/', views.claim_list, name='claim_list'),
    path('create/<int:item_id>/', views.create_claim, name='create_claim'),
    path('owner/', views.owner_claims, name='owner_claims'),
    path('accept/<int:claim_id>/', views.accept_claim, name='accept_claim'),
    path('reject/<int:claim_id>/', views.reject_claim, name='reject_claim'),
]

