# Generated by Django 3.0.8 on 2020-10-25 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0022_auto_20201025_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='tracking',
            field=models.CharField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
