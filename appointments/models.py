from django.db import models
from django.conf import settings
from users.models import CustomUser

class Appointment(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    psychologist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_received')
    datetime = models.DateTimeField()
    message = models.TextField(blank=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_by_psychologist = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.client} -> {self.psychologist} |  {self.datetime}"