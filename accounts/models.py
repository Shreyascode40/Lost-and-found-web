from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    institution = models.ForeignKey(
        "institution.Institution",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_institution = models.BooleanField(default=False)
    is_institution_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
