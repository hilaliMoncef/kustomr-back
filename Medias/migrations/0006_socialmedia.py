# Generated by Django 3.0.6 on 2020-06-22 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Medias', '0005_emailmedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='socials/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
