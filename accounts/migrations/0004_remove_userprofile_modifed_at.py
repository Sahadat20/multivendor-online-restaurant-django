# Generated by Django 4.2.15 on 2024-09-21 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='modifed_at',
        ),
    ]