from django.contrib import admin
from .models import inventory_items_stock,Irumudi_bookig_receipt, Maaladharane, Ghee_Coconut, Temple_seva_receipt,Items_sold_rcpt, Daily_Expense,Donations
# Register your models here.
admin.site.register(inventory_items_stock)
admin.site.register(Irumudi_bookig_receipt)
admin.site.register(Maaladharane)
admin.site.register(Ghee_Coconut)
admin.site.register(Items_sold_rcpt)
admin.site.register(Temple_seva_receipt)
admin.site.register(Daily_Expense)
admin.site.register(Donations)