# Generated by Django 3.0.6 on 2020-05-13 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hello', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friendRequests',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friends', to=settings.AUTH_USER_MODEL),
        ),
    ]