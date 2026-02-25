from django.contrib import admin
from .models import Item
# Register your models here.



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'item_type', 'location', 'date')

    search_fields = ('title', 'description', 'location')

    list_filter = ('item_type', 'date')

    ordering = ('-date',)