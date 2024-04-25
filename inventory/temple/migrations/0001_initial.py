# Generated by Django 5.0.3 on 2024-04-04 18:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Income', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Donations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Contact', models.TextField()),
                ('Amount_Paid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Description', models.TextField()),
                ('Amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ghee_Coconut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Total_Amount', models.IntegerField(default=130)),
                ('Cash', models.IntegerField(default=0)),
                ('UPI', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='inventory_items_stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(max_length=300, unique=True)),
                ('purchase_price', models.IntegerField()),
                ('items_sale_price', models.IntegerField()),
                ('item_sold', models.IntegerField(default=0)),
                ('items_in_stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Irumudi_bookig_receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Contact', models.TextField()),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Irumudi_Price', models.IntegerField()),
                ('Irumudi_Quantity', models.IntegerField()),
                ('Booking_Date', models.DateField(default=datetime.date.today)),
                ('Schedule_Date', models.DateField()),
                ('Scheduled_Time', models.TimeField()),
                ('Amount_Paid', models.IntegerField()),
                ('Balance', models.IntegerField()),
                ('Total_Amount', models.IntegerField()),
                ('Advance_Paid', models.TextField()),
                ('Balance_Clear_Date', models.DateField(blank=True, null=True)),
                ('Balance_Amount_Paid', models.IntegerField(default=0)),
                ('Cash', models.IntegerField(default=0)),
                ('UPI', models.IntegerField(default=0)),
                ('Balance_Receipt_no', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items_sold_rcpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Product_name', models.TextField()),
                ('Total_Amount', models.IntegerField()),
                ('Cash', models.IntegerField(default=0)),
                ('UPI', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Maaladharane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Date', models.DateField(default=datetime.date.today)),
                ('Total_Amount', models.IntegerField(default=15)),
                ('Cash', models.IntegerField(default=0)),
                ('UPI', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Temple_seva_receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Seva_Type', models.CharField(max_length=250)),
                ('Booking_Date', models.DateField(default=datetime.date.today)),
                ('Schedule_Date', models.DateField()),
                ('Receipt_Number', models.CharField(max_length=20, unique=True)),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Contact', models.TextField()),
                ('Total_Amount', models.IntegerField()),
                ('Amount_Paid', models.IntegerField()),
                ('Balance', models.IntegerField()),
            ],
        ),
    ]
