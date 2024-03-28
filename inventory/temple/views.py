from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import inventory_items_stock,Irumudi_bookig_receipt, Maaladharane, Ghee_Coconut, Items_sold_rcpt, Expenses
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
        "Side bag",
        "Doti Blue"
        
    ]
    
    
    if request.method=='POST':
        item=inventory_items_stock.objects

        data=request.POST
        item_name=data.get("items_value")
        purchase_price=int(data.get("purchase_price"))
        items_sale_price=int(data.get("items_sale_price"))
        items_in_stock=int(data.get("items_in_stock"))

        filtered_db=item.filter(items=item_name).exists()
        
        if not filtered_db:       
            # no_of_items_sold=data.get("items_sold")

            # item.update_stock_on_sale(4)
            item_creation=item.create(items=item_name,purchase_price=purchase_price,items_sale_price=items_sale_price,items_in_stock=items_in_stock)
            messages.success(request, 'Your Items were Added successfully')
            return redirect('/update_items')
        else:   
            
            get_item_obj=item.filter(items=item_name)
            my_stocks=get_item_obj.update(purchase_price=purchase_price,items_sale_price=items_sale_price)
            update_row=item.get(items=item_name)
            update_row.update_existing_value(value_update=items_in_stock)

            messages.success(request, 'Your Items were successfully Updated')
            return redirect('/update_items')
       
    return render(request,'temple_app/add_items_list.html',{'list_of_items':items_list})

def irumudi_book(request):

    title="IRUMUDI SCHEDULE"
    cust_data=Irumudi_bookig_receipt.objects
    data=request.POST
    data_recvd={}
    if request.method=="POST":
        my_data={}
        Receipt_Number="IR-" + str(cust_data.count()+ 1 + 1000)
        incoming_request=["Receipt_Number","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Amount_Paid"]
        for i in incoming_request:
            my_data[i]=data.get(i)
            if i=="Receipt_Number":
                my_data[i]=Receipt_Number
      
        total_amount=int(my_data["Irumudi_Price"])*int(my_data["Irumudi_Quantity"])
        balance=total_amount-int(my_data["Amount_Paid"])
        

        calculated_data=["Total_Amount","Balance"]
        str_calculated_data=[total_amount, balance]

        for k,v in zip(calculated_data,str_calculated_data):
            my_data[k]=v


        store_to_db=cust_data.create(**my_data)

        get_data_db=cust_data.filter(Receipt_Number=Receipt_Number)

        rcpt=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Booking_Date")[0]["Booking_Date"]
        
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Amount_Paid","Total_Amount","Balance")[0]

        output_pdf=generate_pdf(title,rcpt,date,cust_info)

        # messages.success(request, 'Information Successfully Added')
        return  output_pdf
        
        # return redirect('/irumudi_recepit')
    return render(request,'temple_app/book_irumudi.html')
    

def items_list(request):
    title="Item Contents"
    items_lists=[ "Mala block spatica 6mm",
        "Mala white spatica 6mm",
        "Mala block spatica 8mm",
        "Mala white spatica 8mm",
        "Towel block 150mm x 100mm",
        "Towel kavi 150mm x 100mm",
        "Doti Black",
        "Doti kavi",
        "Bedsheet",
        "Irumudi bag",
        "Side bag",
        "Doti Blue"
        
    ]
   

    if request.method=="POST":
        data=request.POST
        table=True
        col_list=["Item","Qty","Rate","Amt"]
        if 'add_button' in request.POST :
        
            item_name=data.get("items_value")
            item_qty=data.get("qty")  
            quantity_sold=int(item_qty)   

            found_item=inventory_items_stock.objects.filter(items=item_name)
            price_and_qty=found_item.values("items_sale_price","items_in_stock")
            found_item_price=price_and_qty[0]["items_sale_price"]
            found_item_stock=price_and_qty[0]["items_in_stock"]
            
            particular_amount=found_item_price*quantity_sold

            get_item=inventory_items_stock.objects.get(items=item_name)

            # print(found_item_price,found_item_stock)

            if  found_item_stock < 1:
                messages.error(request,f'{ item_name} OUT OF STOCK')
                return redirect('/irumudi_items')
            else:
                get_item.update_stock_on_sale(quantity_sold=quantity_sold)
            
            session_data=f'{item_name}'
            
            request.session[session_data]=[quantity_sold,found_item_price,particular_amount]

            contents=request.session
            
            
            return render(request,"temple_app/irumudi_items_list.html",{'data':contents,"col":col_list})
            
        
        elif 'submit_button' in request.POST:
            database_obj=Items_sold_rcpt.objects
            Receipt_Number="IL-" + str(database_obj.count()+ 1 + 1000)

            
            item_content=request.session
            total_amount=int()
            product_name=""
            for  key,value in item_content.items():
               price= inventory_items_stock.objects.filter(items=key).values("items_sale_price")[0]["items_sale_price"]
               total_amount+=price*value[0]
               product_name+=f"{key}-{value}, "

            
            store_to_db=database_obj.create(Receipt_Number=Receipt_Number,Total_Amount=total_amount,Product_name=product_name)
            
            fetch_date=database_obj.filter(Receipt_Number=Receipt_Number).values("Date")[0]["Date"]
            
            output_file=generate_pdf(title,Receipt_Number,fetch_date,item_content,total_amount,col_list,table)
            
            request.session.clear()
            request.session.flush()
            return output_file
    
        elif 'check_button' in request.POST:
            item_name=data.get("items_value")
            stock_item=inventory_items_stock.objects.filter(items=item_name).values("items_in_stock")[0]['items_in_stock']
            messages.info(request, f' Only {stock_item} Left In Stock ')
            return redirect('/irumudi_items')
     
    return render(request,"temple_app/irumudi_items_list.html", {"list_of_items":items_lists})
                                                                                                                                                                                                                                                                                                                             
def maaladharane(request):
    title="MAALADHARANE / ARCHANE"
    database_obj=Maaladharane.objects

    if request.method=="POST":
        data=request.POST

        Customer_Name=data.get("Customer_Name")

        Receipt_Number="MD-" + str(database_obj.count()+ 1 + 1000)
    
        store_to_db=database_obj.create(Customer_Name=Customer_Name,Receipt_Number=Receipt_Number)
        
        get_data_db=database_obj.filter(Receipt_Number=Receipt_Number)
        
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Total_Amount")[0]
        rcpt_no=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Date")[0]["Date"]


        output_file=generate_pdf(title,rcpt_no,date,cust_info)
        return  output_file
    
    return render (request, 'temple_app/maaladharane.html')


def ghee(request):
    title="GHEE / COCONUT"
    database_obj=Ghee_Coconut.objects

    if request.method=="POST":
        data=request.POST

        Customer_Name=data.get("Customer_Name")

        Receipt_Number="GC-" + str(database_obj.count()+ 1 + 1000)
    
        store_to_db=database_obj.create(Customer_Name=Customer_Name,Receipt_Number=Receipt_Number)
        
        get_data_db=database_obj.filter(Receipt_Number=Receipt_Number)
        
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Total_Amount")[0]
        rcpt_no=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Date")[0]["Date"]


        output_file=generate_pdf(title,rcpt_no,date,cust_info)
        return  output_file
    
    return render (request, 'temple_app/ghee_recp.html')



def irumudi_register(request):
    to_be_paid=int()
    int_amt_paid=int()
    total_amt=int()

    if 'get_button' in request.POST:
        count=Irumudi_bookig_receipt.objects.filter(Balance__gte=1).count()
        print(count)
        key_col=[]
        data=None
        message=None
        if count>0:
            data=list(Irumudi_bookig_receipt.objects.filter(Balance__gte=1).values())
            
            for k in data[0].keys():
                key_col.append(k)
        else:
            message="No Dues Found !"  
     
        return render (request, 'temple_app/table_record.html',{'data_list':data,'key_set':key_col,'text':message})
        
        # return render (request, 'temple_app/records_irumudi.html',{'data_list':data,'key_set':key_col})
    elif 'search_due' in request.POST:
        Receipt_Number=request.POST.get("Receipt_Number")
        request.session['Receipt_no']=Receipt_Number
        rx_rc=request.session['Receipt_no']
        
        row_fetch=Irumudi_bookig_receipt.objects.filter(Receipt_Number=Receipt_Number).values("Balance","Amount_Paid","Total_Amount")
    
        to_be_paid =Irumudi_bookig_receipt.objects.filter(Receipt_Number=Receipt_Number).values()[0]["Balance"]
       
        if to_be_paid==0:
            messages.info(request,f"No Dues Found For {rx_rc}")
            request.session.flush()
            return redirect('/irumudi_record')       
        
        return render (request, 'temple_app/records_irumudi.html',{'balance':to_be_paid, 'rx_c':rx_rc})
    
    elif 'pay_due_clicked' in request.POST:
        rx_rcpt=request.session["Receipt_no"]
        due=int(request.POST.get("Balance"))
        # print(rx_rcpt,due)

        update_balance=Irumudi_bookig_receipt.objects.get(Receipt_Number=rx_rcpt).amount_update(ap_value=due)
       
        messages.success(request,f" Amount of Rs.{due} Paid ")
        return redirect('/irumudi_record')
    request.session.clear()
    return render (request, 'temple_app/records_irumudi.html')
    

def expenses(request):
    pass_data=["Irumudi","Maaladharane","Ghee/Coconut","Materials"]

    if request.method=="POST":
        data=request.POST
        report_for=data.get("selected_parameter")
        from_date=data.get("from_Date")
        to_date=data.get("to_Date")

        print(from_date,to_date)

        # if report_for=="Irumudi":
        irumudi_cash=Irumudi_bookig_receipt.objects.all().filter(Booking_Date__range=(from_date,to_date))
        irumudi_sale_count=irumudi_cash.count()
        irumudi_cash_values=irumudi_cash.values_list("Receipt_Number","Amount_Paid")
        #print(irumudi_cash_values)

        end_index=irumudi_sale_count-1
        start_rcpt=irumudi_cash_values[0][0]
        end_rcpt=irumudi_cash_values[end_index][0]
        total_cost_in_set_period=0

        for key,val in irumudi_cash_values:
            total_cost_in_set_period+=val
            # print(key,val)

        irumudi_list=[(start_rcpt,end_rcpt),irumudi_sale_count,total_cost_in_set_period]
        print(start_rcpt,end_rcpt,irumudi_sale_count,total_cost_in_set_period)
        
    ## MAALADHARANE
        
        maaladharane_cash=Maaladharane.objects.all().filter(Date__range=(from_date,to_date))
        maaladharane_cash_count=maaladharane_cash.count()

        maaladharane_cash_values=maaladharane_cash.values_list("Receipt_Number","Date","Total_Amount")

        maaladharane_end_index=maaladharane_cash_count-1

        maaladharane_start_rcpt=maaladharane_cash_values[0][0]
        maaladharane_end_rcpt=maaladharane_cash_values[maaladharane_end_index][0]

        total_cost_maaladharne=0
        for k,v,amt in maaladharane_cash_values:
            total_cost_maaladharne+=amt

        print(maaladharane_start_rcpt,maaladharane_end_rcpt,maaladharane_cash_count,total_cost_maaladharne)
        maaladharane_list=[(maaladharane_start_rcpt,maaladharane_end_rcpt),maaladharane_cash_count,total_cost_maaladharne]    

    ## Items_sold_rcpt

        items_sold_rcpt_cash=Items_sold_rcpt.objects.all().filter(Date__range=(from_date,to_date))
        items_sold_rcpt_cash_count=items_sold_rcpt_cash.count()

        items_sold_rcpt_cash_values=items_sold_rcpt_cash.values_list("Receipt_Number","Total_Amount")

        items_sold_end_index=items_sold_rcpt_cash_count-1

        items_startindex=items_sold_rcpt_cash_values[0][0]

        items_endindex=items_sold_rcpt_cash_values[items_sold_end_index][0]

        total_cost_items=0
        for k,v in items_sold_rcpt_cash_values:

            total_cost_items+=v

        print(items_startindex,items_endindex,items_sold_rcpt_cash_count,total_cost_items)
        
        items_data_list=[(items_startindex,items_endindex),items_sold_rcpt_cash_count,total_cost_items]


    ##GheeCoconut

        gc_cash=Ghee_Coconut.objects.all().filter(Date__range=(from_date,to_date))
        gc_cash_count=gc_cash.count()

        gc_cash_values=gc_cash.values_list("Receipt_Number","Date","Total_Amount")

        gc_end_index=gc_cash_count-1

        gc_start_rcpt=gc_cash_values[0][0]
        gc_end_rcpt=gc_cash_values[gc_end_index][0]

        total_cost_gc=0
        for k,v,amt in gc_cash_values:
            total_cost_gc+=amt

        print(gc_start_rcpt,gc_end_rcpt,gc_cash_count,total_cost_gc)
        gc_list=[(gc_start_rcpt,gc_end_rcpt),gc_cash_count,total_cost_gc]    

    # Item Contents
        zipped_data=zip(irumudi_list,maaladharane_list,gc_list,items_data_list)
       
        grand_total=irumudi_list[2]+maaladharane_list[2]+gc_list[2]+items_data_list[2]
        col1=["Receipt Range","Sold","Total Cost"]
        print(grand_total)

        exp_data=Expenses.objects.all().filter(Date__range=(from_date,to_date))
        exp_values=exp_data.values_list("Description","Amount")
        exp_grand_total=0

        for k,v in exp_values:
            exp_grand_total+=v
            print(k,v)

        net_balance=grand_total-exp_grand_total
        return render(request,'temple_app/report_table.html',{"ir_data":irumudi_list,'ml_data': maaladharane_list,"gl_data":gc_list, "id_data":items_data_list,"col1":col1,"from_date":from_date,"to_date":to_date,"items_sold":items_sold_rcpt_cash_values,"irumudi_sold":irumudi_cash_values,"gt":grand_total,"exp_values":exp_values,"grand_total":exp_grand_total,"net_balance":net_balance})
    
    return render(request,'temple_app/cash_report.html',{'my_rcpts':pass_data})
    

def expense(request):
    if request.method=="POST":
        data=request.POST
        Description=data.get("Description")
        Amount=int(data.get("Amount_Spent"))
        store_o_db=Expenses.objects.create(Description=Description,Amount=Amount)

    return render(request,'temple_app/exp_entry.html')

def temple_seva_(request):
    seva_list=["abhisheka","alankara"]

    return render (request, 'temple_app/tmp_seva.html')


def generate_pdf(rcpt_title, rcpt_no,current_date,query_data,total_amt=None,col_name_list=None,table=False):
    
    sl_no=1
    if rcpt_no:
        file_name=f'{rcpt_no}_({current_date}).pdf'
    else:
        file_name=f'Items_sold_({current_date})'.pdf


    header=["                     || Om Sri Swami Sharanam Ayyappa ||        "                         
            ,"  Sri Kaliyuga Varada Ayyappaswamy Temple, Ranganathapura,       ",
            "         Prashanthanagar, 6th Main Road, Bangalore - 79.       "]
    
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename= {0}'.format(file_name)
    y=690
    y2=800
    x=70
    p = canvas.Canvas(response)
    p.setFont("Helvetica", 10)

    if total_amt:
        text=f'Total Amount: Rs.{total_amt}'
        p.drawString(465,680,text)
    p.drawString(242,710,rcpt_title)
    present_date=f'Date : {current_date}'

    p.drawString(480,710,present_date)

    for i in header:
        op=f'{i}'
        p.drawString(165,y2, op)
        y2-=25

    if table:
        y=650
        for col_name in col_name_list:
            res=f'{col_name}'
            p.drawString(x,675, res)
            if col_name=="Item": 
                x+=165
            else:
                x+=35

        for key,value in query_data.items():
            res=f'{sl_no}. {key}'
            res2= f'{value[0]}         {value[1]}        {value[2]}'
            sl_no+=1
            p.drawString(50,y, res)  
            p.drawString(240,y,res2)
            y-=20
    else:        
        for key,value in query_data.items():
            if key=="Total_Amount":
                res=f' {key} : Rs. {value}. '
            
            else:
                
                res=f' {sl_no}. {key} : {value}'
                sl_no+=1

            p.drawString(50,y, res)  
            y-=20
    p.showPage()
    p.save()
    
    return response
