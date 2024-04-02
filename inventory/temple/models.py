
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
    Balance_Clear_Date=models.DateField(null=True,blank=True)
    Balance_Amount_Paid=models.IntegerField(default=0)
    Cash=models.IntegerField(default=0)
    UPI=models.IntegerField(default=0)

    def amount_update(self,ap_value):
        self.Amount_Paid+=ap_value
        self.Balance=self.Balance-ap_value
        self.save()

    def clear_date(self,paid_date):
        self.Balance_Clear_Date=paid_date
        self.save()

    def balance_paid(self,paid_amt):
        self.Balance_Amount_Paid+=paid_amt
        self.save()

    def cash_mode(self,paid_amt):
        self.Cash+=paid_amt
        self.save()

    def upi_mode(self,paid_amt): 
        self.UPI+=paid_amt
        self.save()

    def __str__(self):
        return self.Receipt_Number

class Maaladharane(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Customer_Name=models.CharField(max_length=100)
    Date=models.DateField(default=datetime.date.today)
    Total_Amount=models.IntegerField(default=15)
    Cash=models.IntegerField(default=0)
    UPI=models.IntegerField(default=0)

    def update_cash(self):
        self.Cash=15
        self.save()

    def update_upi(self):
        self.UPI=15
        self.save()

class Ghee_Coconut(models.Model):
    Receipt_Number = models.CharField(max_length=20, unique=True)
    Customer_Name=models.CharField(max_length=100)
    Date=models.DateField(default=datetime.date.today)
    Total_Amount=models.IntegerField(default=130)
    Cash=models.IntegerField(default=0)
    UPI=models.IntegerField(default=0)

    def update_cash(self):
        self.Cash=130
        self.save()

    def update_upi(self):
        self.UPI=130
        self.save()



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
    Cash=models.IntegerField(default=0)
    UPI=models.IntegerField(default=0)

    def update_cash(self,paid_amt):
        self.Cash=paid_amt
        self.save()

    def update_upi(self,paid_amt):
        self.UPI=paid_amt
        self.save()

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