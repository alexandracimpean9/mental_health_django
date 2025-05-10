from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        PSYCHOLOGIST = 'psychologist', 'Psiholog'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
    @property
    def is_psychologist(self):
        return self.role == self.Role.PSYCHOLOGIST
    @property
    def full_name(self):
  
        if self.is_psychologist and hasattr(self, 'psychologist_profile'):
            return self.psychologist_profile.full_name

        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
    
