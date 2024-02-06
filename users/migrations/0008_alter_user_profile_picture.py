# Generated by Django 5.0.1 on 2024-02-06 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='images/default_user.png', null=True, upload_to='profiles/'),
        ),
    ]
