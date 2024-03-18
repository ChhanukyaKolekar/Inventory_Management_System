from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import inventory_items_stock,Irumudi_bookig_receipt
# Create your views here.
import datetime
from django.contrib import messages
from reportlab.pdfgen import canvas

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
def add_items(request):
    
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
        receipt="IR-" + str(cust_data.count()+ 1 + 1000)
        incoming_request=["Receipt_Number","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Amount_Paid"]
        for i in incoming_request:
            my_data[i]=data.get(i)
            if i=="Receipt_Number":
                my_data[i]=receipt
      
        total_amount=int(my_data["Irumudi_Price"])*int(my_data["Irumudi_Quantity"])
        balance=total_amount-int(my_data["Amount_Paid"])
        

        calculated_data=["Total_Amount","Balance"]
        str_calculated_data=[total_amount, balance]

        for k,v in zip(calculated_data,str_calculated_data):
            my_data[k]=v

        print(my_data)

        cust_data.create(**my_data)
        rcpt=my_data["Receipt_Number"]
        
        output_pdf=generate_pdf(rcpt,cust_data,my_data)

        # messages.success(request, 'Information Successfully Added')
        return  output_pdf
        
        # return redirect('/irumudi_recepit')
    return render(request,'temple_app/book_irumudi.html')
    

def items_list(request):
    
    return render(request,"temple_app/irumudi_items_list.html")
    pass                                                                                                                                                                                                                                                                                                                                 
def maaladharane(request):

    return 
    pass

def ghee(request):
    pass

def irumudi_register(request):
    pass

def expenses(request):
    pass

def generate_pdf(rcpt_no,data_obj_db,gen_data):
    data=rcpt_no
    date=data_obj_db.filter(Receipt_Number=data).values("Booking_Date")[0]["Booking_Date"]
    date_obj=data_obj_db.filter(Receipt_Number=data).values_list()

    file_name=f'{data}_({date}).pdf'
    header=["-            || Om Sri Swami Sharanam Ayyappa ||"                         
            ,"Sri Kaliyuga Varada Ayyappaswamy Temple, Ranganathapura,",
            "     Prashanthanagar, 6th Main Road, Bangalore - 79."]
    
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename= {0}'.format(file_name)
    y=700
    y2=800
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 10)
    present_date=f'Date : {date}'
    p.drawString(450,710,present_date)

    for i in header:
        op=f'{i}'
        p.drawString(150,y2, op)
        y2-=25

    for key,value in gen_data.items():
        res=f' {key} : {value} ' 

        p.drawString(50,y, res)  
        y-=20
    p.showPage()
    p.save()
    
    return response