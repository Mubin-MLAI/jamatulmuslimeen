# Generated by Django 4.2.7 on 2023-11-26 20:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jamatulmsl', '0002_contactdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='metainformation',
            name='USERID',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]