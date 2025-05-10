from django.contrib import admin
from .models import Psychologist
from users.models import CustomUser

class PsychologistAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'specialization', 'available']
    fields = ['user', 'full_name', 'specialization', 'description', 'available', 'photo']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = CustomUser.objects.filter(role=CustomUser.Role.PSYCHOLOGIST)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Psychologist, PsychologistAdmin)