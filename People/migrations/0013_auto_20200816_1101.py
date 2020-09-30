# Generated by Django 3.0.8 on 2020-08-16 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('People', '0012_remove_people_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='people_image/'),
        ),
        migrations.AlterField(
            model_name='people',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='people_company', to='People.Company'),
        ),
    ]