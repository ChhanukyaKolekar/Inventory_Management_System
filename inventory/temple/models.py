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
            self.items_sold += quantity_sold
            self.items_in_stock -= quantity_sold
            self.save()
        else:
            pass

    def __str__(self):
        return self.items


    def __str__(self):
        return self.cust_name
    
class Irumudi_bookig_receipt(models.Model):
    receipt_number = models.CharField(max_length=20, unique=True)
    contact_id=models.IntegerField()
    cust_name=models.CharField(max_length=100)
    irumudi_price=models.IntegerField()
    irumudi_qty=models.IntegerField()
    date_created=models.DateField(default=datetime.date.today)
    sch_date=models.DateField()
    paid_amount=models.IntegerField()
    balance=models.IntegerField()
    total_price=models.IntegerField()

    def __str__(self):
        return self.receipt_number

