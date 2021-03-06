# Generated by Django 3.0.8 on 2021-04-28 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rater', models.CharField(max_length=100)),
                ('rate', models.PositiveIntegerField()),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Feedback')),
                ('isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
