# Generated by Django 3.0.4 on 2020-03-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0007_auto_20200328_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')], max_length=140),
        ),
    ]