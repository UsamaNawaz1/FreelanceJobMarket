# Generated by Django 3.1.6 on 2021-06-05 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20210604_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='pending_amount',
        ),
        migrations.AddField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='feedback',
            field=models.CharField(default='', max_length=500),
        ),
    ]
