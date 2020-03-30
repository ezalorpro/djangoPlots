# Generated by Django 3.0.4 on 2020-03-28 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plots', '0006_auto_20200323_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='plots/default.png', upload_to='plots'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('H', 'Hombre'), ('M', 'Mujer')], max_length=140),
        ),
    ]