from django.db import models
from django.contrib.auth.hashers import make_password

class Institution(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    join_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash password if not already hashed
        if not self.join_password.startswith("pbkdf2"):
            self.join_password = make_password(self.join_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
