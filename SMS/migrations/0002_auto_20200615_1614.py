# Generated by Django 3.0.6 on 2020-06-15 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smscampaign',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
