from django.db import models
from django.conf import settings

# Create your models here.

class Item(models.Model):


    ITEM_TYPES = [
        ('Lost', 'Lost'),
        ('Found', 'Found')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPES)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)



    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    institution = models.ForeignKey(
    "institution.Institution",
    on_delete=models.CASCADE
)

    def __str__(self):
        return self.title


