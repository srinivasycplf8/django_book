# Generated by Django 3.0.8 on 2021-04-29 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_auto_20210429_0408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trusted',
            name='person_who_voted',
        ),
        migrations.AlterField(
            model_name='trusted',
            name='person_who_receving',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]