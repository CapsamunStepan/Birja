# Generated by Django 5.1b1 on 2025-04-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programmer', '0005_remove_telegramuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
