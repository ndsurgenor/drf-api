# Generated by Django 3.2.23 on 2023-12-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='../default_profile_n85cdj', upload_to='images/'),
        ),
    ]
