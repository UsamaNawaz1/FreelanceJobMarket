# Generated by Django 3.1.6 on 2021-06-03 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0019_auto_20210603_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobTitle', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('timeCreated', models.DateField(auto_now_add=True, null=True)),
                ('duration', models.CharField(default='', max_length=200)),
                ('experience', models.CharField(default='', max_length=200)),
                ('job_status', models.CharField(default='Open', max_length=200)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
