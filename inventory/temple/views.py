from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import inventory_items_stock,Irumudi_bookig_receipt
# Create your views here.
import datetime
from django.contrib import messages
from reportlab.pdfgen import canvas

def add_items(request):
    items_list=[ "Mala block spatica 6mm",
        "Mala white spatica 6mm",
        "Mala block spatica 8mm",
        "Mala white spatica 8mm",
        "Towel block 150mm x 100mm",
        "Towel kavi 150mm x 100mm",
        "Doti Black",
        "Doti kavi",
        "Bedsheet",
        "Irumudi bag",
        "Side bag"
    ]
    if request.method=='POST':
        item=inventory_items_stock.objects

        data=request.POST
        item_name=data.get("items_value")
        purchase_price=data.get("purchase_price")
        items_sale_price=data.get("items_sale_price")
        items_in_stock=data.get("items_in_stock")

        filtered_db=item.filter(items=item_name).exists()

        if not filtered_db:       
            # no_of_items_sold=data.get("items_sold")

            # item.update_stock_on_sale(4)
            item_creation=item.create(items=item_name,purchase_price=purchase_price,items_sale_price=items_sale_price,items_in_stock=items_in_stock)
            messages.success(request, 'Your Items were Added successfully')
            return redirect('/update_items')
        else:   
            get_item_obj=item.filter(items=item_name)
            my_stocks=get_item_obj.update(purchase_price=purchase_price,items_sale_price=items_sale_price,items_in_stock=items_in_stock)
            messages.success(request, 'Your Items were successfully Updated')
            return redirect('/update_items')
       
    return render(request,'temple_app/add_items_list.html',{'list_of_items':items_list})

def irumudi_book(request):
    cust_data=Irumudi_bookig_receipt.objects
    data=request.POST
    data_recvd={}
    if request.method=="POST":
        my_data={}
        incoming_request=["cust_name","contact_id","irumudi_price","irumudi_qty","sch_date","paid_amount"]
        for i in incoming_request:
            my_data[i]=data.get(i)
      
        total_amount=int(my_data["irumudi_price"])*int(my_data["irumudi_qty"])
        balance=total_amount-int(my_data["paid_amount"])
        receipt="R-" + str(cust_data.count()+ 1 + 1000)

        calculated_data=["total_price","balance","receipt_number"]
        str_calculated_data=[total_amount, balance,receipt]

        for k,v in zip(calculated_data,str_calculated_data):
            my_data[k]=v

        # print(my_data)

        cust_data.create(**my_data)
        rcpt=my_data["receipt_number"]

        output_pdf=generate_pdf(rcpt,cust_data,my_data)
        messages.success(request, 'Information Successfully Added')
        return output_pdf
        
        
        # return redirect('/irumudi_recepit')
    
    

    return render(request,'temple_app/book_irumudi.html')
    

def items_list(request):
    
    return render(request,"temple_app/irumudi_items_list.html")
    pass                                                                                                                                                                                                                                                                                                                                 
def maaladharane(request):
    pass

def ghee(request):
    pass

def irumudi_register(request):
    pass

def expenses(request):
    pass

def generate_pdf(rcpt_no,data_obj,gen_data):
    data=rcpt_no
    # date_obj=data_obj.filter(receipt_number=data).values("date_created")[0]["date_created"]
    date_obj=data_obj.filter(receipt_number=data).values_list()
    
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    y=700
    p = canvas.Canvas(response)
    # op=" Ayappa Temple , vijaynagar"
    for key,value in gen_data.items():
        res=f' {key} : {value} ' 

        p.drawString(150,y, res)  
        y-=20
    p.showPage()
    p.save()
    
    return response