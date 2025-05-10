from django.db import models
from users.models import CustomUser

class Psychologist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, default='CBT')
    description = models.TextField()
    available = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='psychologists_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()