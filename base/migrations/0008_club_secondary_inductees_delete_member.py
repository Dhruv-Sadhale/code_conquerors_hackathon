# Generated by Django 5.0.1 on 2024-04-12 18:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_club_secondary_applicants'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='club_secondary',
            name='inductees',
            field=models.ManyToManyField(blank=True, related_name='inducted_to_clubs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]