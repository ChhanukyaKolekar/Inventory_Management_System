# Generated by Django 4.2.7 on 2024-03-15 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temple', '0002_irumudi_bookig_receipt_receipt_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='receipt_number',
            new_name='Receipt_number',
        ),
    ]