
from django.db import models
from django.utils import timezone
import datetime
# Create your models here.

class inventory_items_stock(models.Model):
    items=models.CharField(max_length=300, unique=True)
    purchase_price=models.IntegerField()
    items_sale_price=models.IntegerField()
    item_sold=models.IntegerField(default=0)
    items_in_stock=models.IntegerField()
    

    def update_stock_on_sale(self, quantity_sold):
        if quantity_sold <= self.items_in_stock:
            self.item_sold += quantity_sold
            self.items_in_stock -= quantity_sold
            self.save()

    def update_existing_value(self,value_update):
        self.items_in_stock+=value_update  
        self.save()

    def __str__(self):
        return self.items

    
class Irumudi_bookig_receipt(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Contact=models.TextField()
    Customer_Name=models.CharField(max_length=100)
    Irumudi_Price=models.IntegerField()
    Irumudi_Quantity=models.IntegerField()
    Booking_Date=models.DateField(default=datetime.date.today)
    Schedule_Date=models.DateField()
    Amount_Paid=models.IntegerField()
    Balance=models.IntegerField()
    Total_Amount=models.IntegerField()

    def amount_update(self,ap_value):
        self.Amount_Paid+=ap_value
        self.Balance-=ap_value
        self.save()

    def __str__(self):
        return self.Receipt_Number

class Maaladharane(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Customer_Name=models.CharField(max_length=100)
    Date=models.DateField(default=datetime.date.today)
    Total_Amount=models.IntegerField(default=15)

class Ghee_Coconut(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Customer_Name=models.CharField(max_length=100)
    Date=models.DateField(default=datetime.date.today)
    Total_Amount=models.IntegerField(default=130)

class Temple_seva_receipt(models.Model):
    Seva_Type=models.CharField(max_length=250)
    Booking_Date=models.DateField(default=datetime.date.today)
    Schedule_Date=models.DateField()
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Customer_Name=models.CharField(max_length=100)
    Contact=models.TextField()
    Total_Amount=models.IntegerField()
    Amount_Paid=models.IntegerField()
    Balance=models.IntegerField()

class Items_sold_rcpt(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Date=models.DateField(default=datetime.date.today)
    Product_name=models.TextField()
    Total_Amount=models.IntegerField()

class Expenses(models.Model):
    Date=models.DateField(default=datetime.date.today)
    Description=models.TextField()
    Amount=models.IntegerField()
    

class Daily_Expense(models.Model):
    Date=models.DateField(default=datetime.date.today)
    Income=models.IntegerField(default=0)

    def daily_update(self,today_balance):
        self.Income+=today_balance
        self.save()


class Donations(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Date=models.DateField(default=datetime.date.today)
    Customer_Name=models.CharField(max_length=100)
    Contact=models.TextField()
    Amount_Paid=models.IntegerField()

    def __str__(self):
        return self.Receipt_Number