# Generated by Django 5.1.6 on 2025-05-02 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_institution_maintenance_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('reason', models.CharField(max_length=255)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_records', to='institutions.institution')),
            ],
        ),
    ]
