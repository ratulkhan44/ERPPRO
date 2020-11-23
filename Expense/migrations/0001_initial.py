# Generated by Django 3.0.8 on 2020-11-17 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accountant', '0021_auto_20201007_1006'),
        ('People', '0025_auto_20201115_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_date', models.DateField()),
                ('particular', models.TextField(blank=True)),
                ('expense_image', models.ImageField(blank=True, null=True, upload_to='expense_image/')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=12)),
                ('expense_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_account', to='Accountant.CreateAccount')),
                ('paid_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_account', to='Accountant.CreateAccount')),
                ('people_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_people_by', to='People.People')),
                ('people_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_people_for', to='People.People')),
            ],
        ),
    ]