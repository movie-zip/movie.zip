# Generated by Django 4.2.8 on 2024-05-20 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img_url',
            field=models.ImageField(default='static/profile_img.jpg', upload_to='user_images/'),
        ),
    ]