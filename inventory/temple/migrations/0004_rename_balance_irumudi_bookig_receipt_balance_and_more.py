# Generated by Django 4.2.7 on 2024-03-15 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temple', '0003_rename_receipt_number_irumudi_bookig_receipt_receipt_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='balance',
            new_name='Balance',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='contact_id',
            new_name='Contact_id',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='cust_name',
            new_name='Cust_name',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='date_created',
            new_name='Date_created',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='irumudi_price',
            new_name='Irumudi_price',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='irumudi_qty',
            new_name='Irumudi_qty',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='paid_amount',
            new_name='Paid_amount',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='sch_date',
            new_name='Schedule_date',
        ),
        migrations.RenameField(
            model_name='irumudi_bookig_receipt',
            old_name='total_price',
            new_name='Total_amount',
        ),
    ]
