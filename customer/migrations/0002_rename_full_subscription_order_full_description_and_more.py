# Generated by Django 5.1b1 on 2025-04-02 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='full_subscription',
            new_name='full_description',
        ),
        migrations.AlterField(
            model_name='order',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
