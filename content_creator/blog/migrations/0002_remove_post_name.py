# Generated by Django 3.2.3 on 2021-08-16 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='name',
        ),
    ]