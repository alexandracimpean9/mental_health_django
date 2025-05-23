# Generated by Django 5.2 on 2025-05-03 14:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Psychologist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('therapies', models.CharField(help_text='Ex: CBT, EMDR, Psihanaliză', max_length=255)),
                ('info', models.TextField(help_text='Descriere generală, formare, experiență etc.')),
                ('is_available', models.BooleanField(default=True, verbose_name='Disponibil pentru programări')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
