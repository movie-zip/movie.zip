# Generated by Django 4.2.8 on 2024-05-19 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='review',
            new_name='note',
        ),
    ]