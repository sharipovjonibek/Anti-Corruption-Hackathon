# Generated by Django 5.1.6 on 2025-05-02 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viloyat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='viloyat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.viloyat'),
        ),
    ]
