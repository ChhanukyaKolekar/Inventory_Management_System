# Generated by Django 5.0.3 on 2024-04-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temple', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irumudi_bookig_receipt',
            name='Scheduled_Time',
            field=models.TextField(),
        ),
    ]
