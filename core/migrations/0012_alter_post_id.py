# Generated by Django 4.1.1 on 2022-10-20 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_post_created_at_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default='<function uuid4 at 0x000001D4E9E87820>', primary_key=True, serialize=False),
        ),
    ]