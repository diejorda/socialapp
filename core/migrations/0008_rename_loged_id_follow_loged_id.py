# Generated by Django 4.1.1 on 2022-10-05 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_loged_di_follow_loged_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='Loged_id',
            new_name='loged_id',
        ),
    ]