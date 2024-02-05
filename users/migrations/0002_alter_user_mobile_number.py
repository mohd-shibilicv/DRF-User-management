# Generated by Django 5.0.1 on 2024-02-02 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(regex='^\\d{10}$')]),
        ),
    ]
