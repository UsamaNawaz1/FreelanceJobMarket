# Generated by Django 3.1.6 on 2021-06-05 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_review_on_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='overall_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
