# Generated by Django 5.1.6 on 2025-05-03 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_maintenancerecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseBreakdown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Kategoriya')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Summasi')),
                ('maintenance_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breakdowns', to='institutions.maintenancerecord')),
            ],
        ),
    ]
