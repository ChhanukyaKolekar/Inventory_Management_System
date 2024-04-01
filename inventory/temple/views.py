from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import inventory_items_stock,Irumudi_bookig_receipt, Maaladharane, Ghee_Coconut, Items_sold_rcpt, Expenses, Daily_Expense, Donations
# Create your views here.
from datetime import datetime
from django.contrib import messages
from reportlab.pdfgen import canvas

global items_list
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
    "Doti Blue",
    "Maale poo rudrakshi"
    
]
def home(request):
    return render(request,'temple_app/home.html')
def add_items(request):
    
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
        
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Total_Amount","Amount_Paid","Balance")[0]

        output_pdf=generate_pdf(title,rcpt,date,cust_info)

        # messages.success(request, 'Information Successfully Added')
        return  output_pdf
        
        # return redirect('/irumudi_recepit')
    return render(request,'temple_app/book_irumudi.html')
    

def items_list_(request):
    title="Item Contents"

    if request.method=="POST":    
        
        data=request.POST
        table=True
        act=data.get("action")
        col_list=["Item","Qty","Rate","Amt"]
        if 'add_button' in request.POST:    
            item_name=data.get("items_value")
            item_qty=data.get("qty")  
            quantity_sold=int(item_qty)   

            found_item=inventory_items_stock.objects.filter(items=item_name)
            price_and_qty=found_item.values("items_sale_price","items_in_stock")
            print("PandQ",price_and_qty )
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
            print(contents)
            return render(request,"temple_app/irumudi_items_list.html",{'data':contents,"col":col_list,"list_of_items":items_list})
            
        
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
            request.session.flush()
            return output_file
    
        elif 'check_button' in request.POST:
            item_name=data.get("items_value")
            stock_item=inventory_items_stock.objects.filter(items=item_name).values("items_in_stock")[0]['items_in_stock']
            messages.info(request, f' Only {stock_item} Left In Stock ')
            return redirect('/irumudi_items')
        elif 'finish' in request.POST:
            request.session.flush()
    return render(request,"temple_app/irumudi_items_list.html", {"list_of_items":items_list})
                                                                                                                                                                                                                                                                                                                             
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
        
        from_Date=data.get("from_Date")
        to_Date=data.get("to_Date")

        ir_result,ir_cash_value=ir_fun(from_Date,to_Date)

        ml_result=mal_fun(from_Date,to_Date)

        il_result,il_cash_value=il_fun(from_Date,to_Date)

        gc_result=gc_fun(from_Date,to_Date)
        
        donation_lst,donation_info=donate_fun(from_Date,to_Date)
        donate_amt=donation_lst[2]
        print("...............total_d",donate_amt)
        zipped_data=[ir_result,ml_result,gc_result,il_result]
        
        grand_total_=0
        for i in zipped_data:
            grand_total_+=fetch_2_index(i)

        grand_total_+=donate_amt
        net_result,exp_values,exp_grand_total=exp_fun(from_Date,to_Date,grand_total_)

        col1=["Receipt Range","Sold","Total Cost"]
        col2=["Receipt Range","Total Donation"]

        print(ir_result,ml_result,gc_result,il_result, grand_total_)

        # net_total_today=daily_fun(net_result)

        return render(request,'temple_app/report_table.html',{"ir_data":ir_result,'ml_data': ml_result,"gl_data":gc_result, "id_data":il_result,"col1":col1,"from_date":from_Date,"to_date":to_Date,"items_sold":il_cash_value,"irumudi_sold":ir_cash_value,"gt":grand_total_,"exp_values":exp_values,"grand_total":exp_grand_total,"net_balance":net_result,"col2":col2,"donation_amt":donation_lst,"donation_values":donation_info})
    
    return render(request,'temple_app/cash_report.html',{'my_rcpts':pass_data})
    

def expense(request):
    if request.method=="POST":
        data=request.POST
        Description=data.get("Description")
        Amount=int(data.get("Amount_Spent"))
        store_o_db=Expenses.objects.create(Description=Description,Amount=Amount)

    return render(request,'temple_app/exp_entry.html')

def scheduled_irumudi(request):
    if request.method=='POST':
        data=request.POST
        from_date=data.get("from_Date")
        to_date=data.get("to_Date")
        key_col=[]
        fetch_data=None
        message=None
    
        fetch_data=Irumudi_bookig_receipt.objects.filter(Schedule_Date__range=(from_date,to_date)).values()
        print("TRY WAS CALLED",fetch_data)
        if not fetch_data.exists():
            print("Not exist")
            message=f"No Schedules from {from_date} to {to_date}"
            return render (request, 'temple_app/table_record.html',{'data_list':fetch_data,'key_set':key_col,'text':message})
        for k in fetch_data[0].keys():
            key_col.append(k)
        print(key_col)
        return render (request, 'temple_app/table_record.html',{'data_list':fetch_data,'key_set':key_col,'text':message,'from_date':from_date,'to_date':to_date})    

    return render(request,'temple_app/scheduled_list_irumudi.html')

def donate(request):
    rcpt_title="Donation"
    if request.method=="POST":
        data=request.POST
        Customer_Name=data.get("Customer_Name")
        Contact=data.get("Contact")
        Amount_Paid=data.get("Amount_Paid")

        database_obj=Donations.objects
        Receipt_Number="DN-" + str(database_obj.count()+ 1 + 1000)
        store_to_db=database_obj.create(Receipt_Number=Receipt_Number,Customer_Name=Customer_Name,Contact=Contact,Amount_Paid=Amount_Paid)
        donation_db=database_obj.filter(Receipt_Number=Receipt_Number)
        donation_info=donation_db.values("Receipt_Number","Customer_Name","Contact","Amount_Paid")[0]
        rcpt_no=donation_db.values("Receipt_Number")[0]["Receipt_Number"]

        pr_date=donation_db.values("Date")[0]["Date"]
        out=generate_pdf(rcpt_title,rcpt_no,pr_date,donation_info)
        print(donation_db)
        return out
       
    return render(request,'temple_app/donation.html')


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
            if key=="Total_Amount" :
                res=f' {key} : Rs. {value}. '
            elif key== "Amount_Paid":
                res=f' {key} : Rs. {value}. '

            elif key=="Balance":      
                res=f' {key} : Rs. {value}. '
            else:
                
                res=f' {sl_no}. {key} : {value}'
                sl_no+=1

            p.drawString(50,y, res)  
            y-=20
    p.showPage()
    p.save()
    
    return response


def ir_fun(from_date,to_date):
    try:
        irumudi_cash=Irumudi_bookig_receipt.objects.all().filter(Booking_Date__range=(from_date,to_date))
        if not irumudi_cash.exists():
            irumudi_list=[]
            return irumudi_list,None

    except:
        irumudi_cash=Irumudi_bookig_receipt.objects.all().filter(Booking_Date=from_date)
        if not irumudi_cash.existst():
            irumudi_list=[]
            return irumudi_list,None
        
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
    return irumudi_list,irumudi_cash_values
    print(start_rcpt,end_rcpt,irumudi_sale_count,total_cost_in_set_period)


def mal_fun(from_date,to_date):
    ## MAALADHARANE
    try:
        maaladharane_cash=Maaladharane.objects.all().filter(Date__range=(from_date,to_date))
        if not maaladharane_cash.exists():
            maaladharane_list=[]
            return maaladharane_list
    except:
        maaladharane_cash=Maaladharane.objects.all().filter(Date=from_date)
        if not maaladharane_cash.exists():
            print("ML INVALID")
            maaladharane_list=[]
            return maaladharane_list
        
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
    return maaladharane_list

def il_fun(from_date,to_date):
    
    ## Items_sold_rcpt
    try:
        items_sold_rcpt_cash=Items_sold_rcpt.objects.all().filter(Date__range=(from_date,to_date))
        if not items_sold_rcpt_cash.exists():
            items_data_list=[]
            return items_data_list,None
    except: 
        items_sold_rcpt_cash=Items_sold_rcpt.objects.all().filter(Date=from_date)
        if not items_sold_rcpt_cash.exists():
            items_data_list=[]
            return items_data_list,None

    items_sold_rcpt_cash_count=items_sold_rcpt_cash.count()

    items_sold_rcpt_cash_values=items_sold_rcpt_cash.values_list("Receipt_Number","Total_Amount")

    items_sold_end_index=items_sold_rcpt_cash_count-1
    print(items_sold_rcpt_cash_values)

    items_startindex=items_sold_rcpt_cash_values[0][0]

    items_endindex=items_sold_rcpt_cash_values[items_sold_end_index][0]

    total_cost_items=0
    for k,v in items_sold_rcpt_cash_values:
        total_cost_items+=v

    print(items_startindex,items_endindex,items_sold_rcpt_cash_count,total_cost_items)
    
    items_data_list=[(items_startindex,items_endindex),items_sold_rcpt_cash_count,total_cost_items]
    return items_data_list,items_sold_rcpt_cash_values

def gc_fun(from_date,to_date):
    
##GheeCoconut
    try:
        gc_cash=Ghee_Coconut.objects.all().filter(Date__range=(from_date,to_date))
        if not gc_cash.exists():
            gc_list=[]
            return gc_list

    except:
        gc_cash=Ghee_Coconut.objects.all().filter(Date=from_date)
        if not gc_cash.exists():
            gc_list=[]
            return gc_list

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
    return gc_list

def exp_fun(from_date,to_date,grand_total):
    try:
        exp_data=Expenses.objects.all().filter(Date__range=(from_date,to_date))
        if not exp_data.exists():
            return None,None,None
    except:
        exp_data=Expenses.objects.all().filter(Date=from_date)
        if not exp_data.exists():
            return None,None,None

    exp_values=exp_data.values_list("Description","Amount")
    exp_grand_total=0

    for k,v in exp_values:
        exp_grand_total+=v
        print(k,v)

    net_balance=grand_total-exp_grand_total
    return net_balance,exp_values,exp_grand_total

def daily_fun(net_balance):
    income_col=None
    date_col=None

    # try:
    #     store_net_balance=Daily_Expense.daily_update(today_balance=net_balance)
        
    # except:
    #     Daily_Expense.objects.create(Income=net_balance)
    
    last_row=Daily_Expense.objects.last()
    income_col=last_row.Income
    date_col=last_row.Date
    
    prsent=datetime.now()
    pr_date=prsent.date()
  
    print("############my_income", income_col,date_col,prsent,pr_date)

    if date_col==pr_date:
        print("Yes Equal")
        db=Daily_Expense.objects.filter(Date=date_col)
        db_inst=Daily_Expense.objects.get(Date=date_col)
        op=db.values_list("Date","Income")[0]
        db_date=op[0]
        db_income=op[1]

        if db_income!=net_balance:
            print("unequal")
            update_row= db_inst.daily_update(today_balance=net_balance)
            up_value=db.values_list("Income")[0][0]
            print(db_date,db_income,up_value)
            return up_value
        print(db_date,db_income)
        return db_income
    else:
        prev_day=income_col+net_balance
        Daily_Expense.objects.create(Income=prev_day)
        fresh_row=Daily_Expense.objects.last()
        curr_net_balnce=fresh_row.Income
        print(curr_net_balnce)
        return curr_net_balnce
    
def donate_fun(from_date,to_date):
    fetch_data=Donations.objects.filter(Date__range=(from_date,to_date))
    if not fetch_data.exists():
        return None
    print("Donation Available")
    db_values=fetch_data.values_list("Receipt_Number","Amount_Paid")
    db_count=fetch_data.count()
    db_end_index=db_count-1
    total_donation=0
    start_index=db_values[0][0]
    end_index=db_values[db_end_index][0]

    for rc,amt in db_values:
        total_donation+=amt
    print(total_donation)
    donation_list=[(start_index,end_index),db_count,total_donation]
    return donation_list,db_values
   


def fetch_2_index(list_of_lists):
    
    if list_of_lists==[]:
        return 0
    else:
        return list_of_lists[2]
    
