# Generated by Django 3.0.4 on 2020-03-24 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0004_auto_20200323_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='default.jpg', upload_to='plots'),
        ),
    ]