# Generated by Django 4.2.7 on 2023-11-24 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jamatulmsl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactdetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('phoneno', models.CharField(max_length=12)),
                ('msg', models.TextField()),
            ],
            options={
                'db_table': 'Contact_Us',
            },
        ),
    ]
