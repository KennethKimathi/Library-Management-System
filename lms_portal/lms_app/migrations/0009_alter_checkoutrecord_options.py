# Generated by Django 5.1.1 on 2024-10-01 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms_app', '0008_alter_checkoutrecord_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkoutrecord',
            options={'verbose_name': 'CheckoutRecord', 'verbose_name_plural': 'CheckoutRecords'},
        ),
    ]
