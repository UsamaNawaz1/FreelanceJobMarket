# Generated by Django 3.1.6 on 2021-06-03 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0015_useraward'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='feedback',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_rating', models.IntegerField(default=0)),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='givenby', to=settings.AUTH_USER_MODEL)),
                ('given_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='givento', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
