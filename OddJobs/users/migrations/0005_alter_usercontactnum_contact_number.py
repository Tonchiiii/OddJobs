# Generated by Django 4.1.7 on 2023-05-19 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usercontactnum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercontactnum',
            name='contact_number',
            field=models.CharField(max_length=20),
        ),
    ]