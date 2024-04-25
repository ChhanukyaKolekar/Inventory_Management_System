from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect,FileResponse
from django.urls import reverse
from . models import inventory_items_stock,Irumudi_bookig_receipt, Maaladharane, Ghee_Coconut, Items_sold_rcpt, Expenses, Daily_Expense, Donations
# Create your views here.
from datetime import datetime
from django.contrib import messages
from reportlab.pdfgen import canvas
import os
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
            messages.success(request, 'Added successfully')
            return redirect('/update_items')
        else:   
            
            get_item_obj=item.filter(items=item_name)
            my_stocks=get_item_obj.update(purchase_price=purchase_price,items_sale_price=items_sale_price)
            update_row=item.get(items=item_name)
            update_row.update_existing_value(value_update=items_in_stock)

            messages.success(request, 'Updated Successfully ')
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
        incoming_request=["Receipt_Number","Customer_Name","Contact","Irumudi_Quantity","Schedule_Date","Scheduled_Time","Amount_Paid"]
        pay_mode=data.get("Payment_Mode")
        for i in incoming_request:
            my_data[i]=data.get(i)
            if i=="Receipt_Number":
                my_data[i]=Receipt_Number

      
        # total_amount=int(my_data["Irumudi_Price"])*int(my_data["Irumudi_Quantity"])

        # amt_paid=int(my_data["Amount_Paid"])

      
        # balance=total_amount-amt_paid
        # calculated_data=["Total_Amount","Balance"]
        # str_calculated_data=[total_amount, balance]

        # for k,v in zip(calculated_data,str_calculated_data):
        #     my_data[k]=v

        store_to_db=cust_data.create(**my_data)
       
        get_data_db=cust_data.filter(Receipt_Number=Receipt_Number)
        updating_row=cust_data.get(Receipt_Number=Receipt_Number)
        updating_row.total_amt_update()

        prsent=datetime.now()
        pr_date=prsent.date()

        total_amount_and_amt_paid=get_data_db.values_list("Total_Amount","Amount_Paid")
        total_amount=total_amount_and_amt_paid[0][0]
        amt_paid=total_amount_and_amt_paid[0][1]
        updating_row.balance_update(amt_paid)


        if pay_mode=="cash":
            updating_row.cash_mode(paid_amt=amt_paid)
            if amt_paid==total_amount:
                txt=f'0'
                updating_row.adv_pay(paid_amt=txt)
                updating_row.clear_date(paid_date=pr_date)
            else:
                txt=f'{amt_paid} Cash'
                # print(txt)
                updating_row.adv_pay(paid_amt=txt)
                
        else:
            updating_row.upi_mode(paid_amt=amt_paid)
            if amt_paid==total_amount:
                txt=f'0'
                updating_row.adv_pay(paid_amt=txt)
                updating_row.clear_date(paid_date=pr_date)
            else:
                txt=f'{amt_paid} UPI'
                updating_row.adv_pay(paid_amt=txt)


        rcpt=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Booking_Date")[0]["Booking_Date"]

        
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Scheduled_Time","Total_Amount","Amount_Paid","Balance")[0]
        
        file_path=f'C:\\Users\\CHHANUKYA STARK\\OneDrive\\Documents\\All_Receipts\\Irumudi_Bookings\\{rcpt}_({date}).pdf'
        output_pdf=generate_pdf(file_path,title,rcpt,date,cust_info)

        messages.success(request, 'Booking Successfull')
        
        return  redirect('irumudi_book')
        
        # return redirect('/irumudi_recepit')
    return render(request,'temple_app/book_irumudi.html')
    

def items_list_(request):
    title="ITEMS CONTENTS"

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
            
            
            session_data=f'{item_name}'
            
            request.session[session_data]=[quantity_sold,found_item_price,particular_amount]

            contents=request.session
            print(contents)
            return render(request,"temple_app/irumudi_items_list.html",{'data':contents,"col":col_list,"list_of_items":items_list})
            
        
        elif 'submit_button' in request.POST:
            database_obj=Items_sold_rcpt.objects
            Receipt_Number="ML-" + str(database_obj.count()+ 1 + 1000)  
            item_content=request.session
            pay_mode=request.POST.get("Payment_Mode")

            total_amount=int()
            product_name=""
            quantity_sold=int()
            for  key,value in item_content.items():
               price= inventory_items_stock.objects.filter(items=key).values("items_sale_price")[0]["items_sale_price"]
               update_stock=inventory_items_stock.objects.get(items=key)
               update_stock.update_stock_on_sale(quantity_sold=value[0])
               total_amount+=price*value[0]
               product_name+=f"{key}-{value}, "
               quantity_sold

            
            store_to_db=database_obj.create(Receipt_Number=Receipt_Number,Total_Amount=total_amount,Product_name=product_name)
            update_row=database_obj.get(Receipt_Number=Receipt_Number)
            
            

            if pay_mode=="cash":
                update_row.update_cash(paid_amt=total_amount)
            else:
                update_row.update_upi(paid_amt=total_amount)

            fetch_date=database_obj.filter(Receipt_Number=Receipt_Number).values("Date")[0]["Date"]
            file_path=f'C:\\Users\\CHHANUKYA STARK\\Documents\\All_Receipts\\MATERIALS\\{Receipt_Number}_({fetch_date}).pdf'
            output_file=generate_pdf(file_path,title,Receipt_Number,fetch_date,item_content,total_amount,col_list,table)
            request.session.flush()
            messages.success(request, 'Materials Added Successfully ')
            return redirect('/irumudi_items')
    
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
        pay_mode=data.get("Payment_Mode")
        Receipt_Number="MD-" + str(database_obj.count()+ 1 + 1000)
    
        store_to_db=database_obj.create(Customer_Name=Customer_Name,Receipt_Number=Receipt_Number)
        
        get_data_db=database_obj.filter(Receipt_Number=Receipt_Number)
        update_row=database_obj.get(Receipt_Number=Receipt_Number)
        if pay_mode=="cash":
            update_row.update_cash()
        else:
            update_row.update_upi()

        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Total_Amount")[0]
        rcpt_no=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Date")[0]["Date"]

        file_path=f'C:\\Users\\CHHANUKYA STARK\\Documents\\All_Receipts\\Maaladharane_and_Archane\\{rcpt_no}_({date}).pdf'

        output_file=generate_pdf(file_path,title,rcpt_no,date,cust_info)

        messages.success(request, 'Submission Successfull')
        return redirect('maaladharane')
    
    return render (request, 'temple_app/maaladharane.html')


def ghee(request):
    title="GHEE / COCONUT"
    database_obj=Ghee_Coconut.objects

    if request.method=="POST":
        data=request.POST

        Customer_Name=data.get("Customer_Name")
        pay_mode=data.get("Payment_Mode")

        Receipt_Number="GC-" + str(database_obj.count()+ 1 + 1000)
    
        store_to_db=database_obj.create(Customer_Name=Customer_Name,Receipt_Number=Receipt_Number)
        
        get_data_db=database_obj.filter(Receipt_Number=Receipt_Number)
        update_row=database_obj.get(Receipt_Number=Receipt_Number)
        if pay_mode=="cash":
            update_row.update_cash()
        else:
            update_row.update_upi()
        cust_info=get_data_db.values("Receipt_Number","Customer_Name","Total_Amount")[0]
        rcpt_no=get_data_db.values("Receipt_Number")[0]["Receipt_Number"]

        date=get_data_db.values("Date")[0]["Date"]

        file_path=f'C:\\Users\\CHHANUKYA STARK\\Documents\\All_Receipts\\Ghee_Coconut\\{rcpt_no}_({date}).pdf'
        output_file=generate_pdf(file_path,title,rcpt_no,date,cust_info)
        messages.success(request, 'Submission Successfull')
        return  redirect('ghee')
    
    return render (request, 'temple_app/ghee_recp.html')



def irumudi_register(request):
    to_be_paid=int()
    int_amt_paid=int()
    total_amt=int()
    prsent=datetime.now()
    pr_date=prsent.date()
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
        title="BALANCE PAID RECEIPT"

        rx_rcpt=request.session["Receipt_no"]
        due=int(request.POST.get("Balance"))
        # print(rx_rcpt,due)
        pay_mode=request.POST.get("Payment_Mode")
        prsent=datetime.now()
        pr_date=prsent.date()

        update_row=Irumudi_bookig_receipt.objects.get(Receipt_Number=rx_rcpt)
        update_amt_paid=update_row.amount_update(ap_value=due)

        update_bal_date=update_row.clear_date(paid_date=pr_date)
        update_bal_paid=update_row.balance_paid(paid_amt=due)
        balance_rcpt_no=f'BRN-{rx_rcpt}'
        update_row.balance_rcpt(no=balance_rcpt_no)

        if pay_mode=="cash":
            update_row.cash_mode(paid_amt=due)
            txt="Cash"
            update_row.bal_pay_mode(mode=txt)
        else:
            txt="UPI"
            update_row.bal_pay_mode(mode=txt)
            update_row.upi_mode(paid_amt=due)
        
        get_all_obj=Irumudi_bookig_receipt.objects.filter(Receipt_Number=rx_rcpt)
        get_info=get_all_obj.values("Balance_Receipt_no","Customer_Name","Contact","Irumudi_Price","Irumudi_Quantity","Schedule_Date","Scheduled_Time","Total_Amount","Amount_Paid","Balance_Amount_Paid","Advance_Paid","Balance")[0]
        get_date=get_all_obj.values("Balance_Clear_Date")[0]["Balance_Clear_Date"]
        get_BNR_no=get_all_obj.values("Balance_Receipt_no")[0]["Balance_Receipt_no"]
        
        file_path=f'C:\\Users\\CHHANUKYA STARK\\Documents\\All_Receipts\\Balace_Receipts\\{get_BNR_no}_({get_date}).pdf'
        closure_pdf=generate_pdf(file_path,title,get_BNR_no,get_date,get_info)
    
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

        ir_result,ir_cash_value,ir_result2,ir_cash_value2=ir_fun(from_Date,to_Date)
        # print("fun result",ir_result,ir_result2)
        ml_result=mal_fun(from_Date,to_Date)

        il_result,il_cash_value=il_fun(from_Date,to_Date)

        gc_result=gc_fun(from_Date,to_Date)
        # print(gc_result)

        donation_lst,donation_info=donate_fun(from_Date,to_Date)

        if donation_lst!=[]:
            donate_amt=donation_lst[2]
        else:
            donate_amt=0
       
        zipped_data=[ir_result,ml_result,gc_result,il_result,donation_lst]
        zip2=[ir_result2]
        print(ir_result,ml_result,gc_result,il_result,donation_lst)
        # print(ir_result,ir_result2,ir_cash_value,ir_cash_value2)

       
        grand_total_=0
        cash_grand_total_1=0
        upi_grand_total_1=0

        for i in zipped_data:
            gt,csh,upi=fetch_index(i)
            grand_total_+=gt
            cash_grand_total_1+=csh
            upi_grand_total_1+=upi

        cash_grand_total_2=0
        upi_grand_total_2=0
        grand_total_2=0
        
        for i in zip2:
            gt,csh,upi=fetch_index(i)
            grand_total_2+=gt
            cash_grand_total_2+=csh
            upi_grand_total_2+=upi
        print(grand_total_,grand_total_2)

        grand_total_+=grand_total_2
        cash_grand_total_1+=cash_grand_total_2
        upi_grand_total_1+= upi_grand_total_2
        
        
        overall_grand_total=grand_total_
        net_result,exp_values,exp_grand_total=exp_fun(from_Date,to_Date,overall_grand_total)

        col1=["Receipt Range","Sold","Total Cost","Cash","UPI"]
        col2=["Receipt Range","Total Donation"]


        return render(request,'temple_app/report_table.html',{"ir_data":ir_result,'ml_data': ml_result,"gl_data":gc_result, "id_data":il_result,"col1":col1,"from_date":from_Date,"to_date":to_Date,"items_sold":il_cash_value,"irumudi_sold":ir_cash_value,"gt":grand_total_,"exp_values":exp_values,"grand_total":exp_grand_total,"net_balance":net_result,"col2":col2,"donation_amt":donation_lst,"donation_values":donation_info,"ir_data2":ir_result2,"irumudi_sold2":ir_cash_value2,"cash_gt_1":cash_grand_total_1,"upi_gt_1":upi_grand_total_1,"cash_gt_2":cash_grand_total_2,"upi_gt_2":upi_grand_total_2,"gt_2":grand_total_2,"ogt":overall_grand_total})
    
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
    rcpt_title="DONATION"
    if request.method=="POST":
        data=request.POST
        Customer_Name=data.get("Customer_Name")
        Contact=data.get("Contact")
        Amount_Paid=data.get("Amount_Paid")
        Payment_Mode=data.get("Payment_Mode")

        database_obj=Donations.objects
        Receipt_Number="DN-" + str(database_obj.count()+ 1 + 1000)

        store_to_db=database_obj.create(Receipt_Number=Receipt_Number,Customer_Name=Customer_Name,Contact=Contact,Amount_Paid=Amount_Paid)
        get_obj=database_obj.get(Receipt_Number=Receipt_Number)
        if Payment_Mode=="cash":
            get_obj.update_cash(paid_amt=Amount_Paid)
        else:
            get_obj.update_upi(paid_amt=Amount_Paid)
        donation_db=database_obj.filter(Receipt_Number=Receipt_Number)


        donation_info=donation_db.values("Receipt_Number","Customer_Name","Contact","Amount_Paid")[0]
        rcpt_no=donation_db.values("Receipt_Number")[0]["Receipt_Number"]

        pr_date=donation_db.values("Date")[0]["Date"]
        
        file_path=f'C:\\Users\\CHHANUKYA STARK\\Documents\\All_Receipts\\Donations\\{rcpt_no}_({pr_date}).pdf'
        out=generate_pdf(file_path,rcpt_title,rcpt_no,pr_date,donation_info,None,None,False,True)
        print(donation_db)
        messages.success(request, 'Donation Successfull')
        return redirect('donate')
       
    return render(request,'temple_app/donation.html')


def generate_pdf(file_path,rcpt_title,rcpt_no,current_date,query_data,total_amt=None,col_name_list=None,table=False,dn=False):
   
    sl_no=1
    # if rcpt_no:

    #     file_name=f'{rcpt_no}_({current_date}).pdf'
    # else:
    #     file_name=f'Items_sold_({current_date}).pdf'

    header=["                     || Om Sri Swami Sharanam Ayyappa ||        "                         
            ,"  Sri Kaliyuga Varada Ayyappaswamy Temple, Ranganathapura,       ",
            "         Prashanthanagar, 6th Main Road, Bangalore - 79.       "]
    
    # response = HttpResponse(content_type='application/pdf')

    # response['Content-Disposition'] = 'attachment; filename= {0}'.format(file_name)

    y=690
    y2=800
    x=70
    p = canvas.Canvas(file_path)
    p.setFont("Helvetica", 10)
    if dn:
        text=f'THANKS FOR YOUR CONTRIBUTION'
        p.drawString(200,600,text)

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

            elif key=="Balance_Amount_Paid":
                res=f' {key} : Rs. {value}. '
            elif key=="Advance_Paid":
                res=f' {key} : Rs. {value}. '

            else:
                
                res=f' {sl_no}. {key} : {value}'
                sl_no+=1

            p.drawString(50,y, res)  
            y-=20
    p.showPage()
    p.save()
    # print("pdf_res",response)
    


def ir_fun(from_date,to_date):
    irumudi_list=[]
    irumudi_cash_values=[]

    irumudi_list2=[]
    irumudi_cash_values2=[]
    date_object = datetime.strptime(from_date, '%Y-%m-%d').date()
    date_object2 = datetime.strptime(to_date, '%Y-%m-%d').date()
    
    irumudi_cash=Irumudi_bookig_receipt.objects.all().filter(Booking_Date__range=(from_date,to_date))
    irumudi_2_cash=Irumudi_bookig_receipt.objects.all().filter(Balance_Clear_Date__range=(from_date,to_date))
    try:
       
        # print("I AWS CALLED IR",irumudi_2_cash,irumudi_cash)

        if irumudi_cash.exists():
            irumudi_sale_count=irumudi_cash.count()
            irumudi_cash_values=irumudi_cash.values_list("Receipt_Number","Balance_Clear_Date","Amount_Paid","Cash","UPI","Advance_Paid")
            print(irumudi_cash_values)

            end_index=irumudi_sale_count-1
            start_rcpt=irumudi_cash_values[0][0]
            end_rcpt=irumudi_cash_values[end_index][0]

            total_cost_in_set_period=0
            cash_amt=0
            upi_amt=0

            for key,bcd,val,csh,upi,advp in irumudi_cash_values:
                if key!= None:   
                    total_cost_in_set_period+=val
                    cash_amt+=csh
                    upi_amt+=upi
                    # irumudi_cash_values=irumudi_cash.values_list("Receipt_Number","Balance_Clear_Date","Amount_Paid","Cash","UPI","Advance_Paid")
            
                elif bcd>date_object2:
                    val_spli=int(advp.split()[0])
                    total_cost_in_set_period+=val_spli
                    # irumudi_cash_values=irumudi_cash.values_list("Receipt_Number","Balance_Clear_Date","Advance_Paid","Cash","UPI","Amount_Paid")
                    continue
                
                elif bcd==None:
                    val_spli=int(advp.split()[0])
                    mode=advp.split()[1]
                    total_cost_in_set_period+=val_spli
                    # irumudi_cash_values=irumudi_cash.values_list("Receipt_Number","Balance_Clear_Date","Advance_Paid","Cash","UPI","Amount_Paid")
                    if mode=='Cash':
                        cash_amt+=csh
                    else:
                        upi_amt+=upi
                    continue
               
            irumudi_list=[(start_rcpt,end_rcpt),irumudi_sale_count,total_cost_in_set_period,cash_amt,upi_amt]
            # print(start_rcpt,end_rcpt,irumudi_sale_count,total_cost_in_set_period)
        
        if irumudi_2_cash.exists():
            print("2 was called ")
            irumudi_sale_count2=irumudi_2_cash.count()
            irumudi_cash_values2=irumudi_2_cash.values_list("Balance_Receipt_no","Balance_Amount_Paid","Balance_Amount_Payment_Mode","Booking_Date","Balance_Clear_Date")

            print(irumudi_2_cash)

            end_index2=irumudi_sale_count2-1
            start_rcpt2=irumudi_cash_values2[0][0]

            end_rcpt2=irumudi_cash_values2[end_index2][0]

            total_cost_in_set_period2=0
            cash_amt2=0
            upi_amt2=0
            
            for key,val,pay_mode,bkd,bcd in irumudi_cash_values2:
               
                if (bkd==bcd)  :
                    total_cost_in_set_period2+=0
                    continue
                elif (bcd>date_object) :
                    total_cost_in_set_period2+=0
                    continue

                total_cost_in_set_period2+=val
                if pay_mode=="Cash":
                    cash_amt2+=val
                elif pay_mode=="UPI":
                    upi_amt2+=val
                # print(key,val)

            irumudi_list2=[(start_rcpt2,end_rcpt2),irumudi_sale_count2,total_cost_in_set_period2,cash_amt2,upi_amt2]
            print(irumudi_list2)

        # print("try_block",irumudi_list,irumudi_cash_values,irumudi_list2,irumudi_cash_values2)
        return irumudi_list,irumudi_cash_values,irumudi_list2,irumudi_cash_values2
    except:
        return irumudi_list,irumudi_cash_values,irumudi_list2,irumudi_cash_values2
       
            

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
            # print("ML INVALID")
            maaladharane_list=[]
            return maaladharane_list
        
    maaladharane_cash_count=maaladharane_cash.count()

    maaladharane_cash_values=maaladharane_cash.values_list("Receipt_Number","Date","Total_Amount","Cash","UPI")

    maaladharane_end_index=maaladharane_cash_count-1

    maaladharane_start_rcpt=maaladharane_cash_values[0][0]
    maaladharane_end_rcpt=maaladharane_cash_values[maaladharane_end_index][0]

    total_cost_maaladharne=0
    cash_amt=0
    upi_amt=0

    for k,v,amt,csh,upi in maaladharane_cash_values:
        total_cost_maaladharne+=amt
        cash_amt+=csh
        upi_amt+=upi

    # print(maaladharane_start_rcpt,maaladharane_end_rcpt,maaladharane_cash_count,total_cost_maaladharne)
    maaladharane_list=[(maaladharane_start_rcpt,maaladharane_end_rcpt),maaladharane_cash_count,total_cost_maaladharne,cash_amt,upi_amt]    
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

    items_sold_rcpt_cash_values=items_sold_rcpt_cash.values_list("Receipt_Number","Total_Amount","Cash","UPI")

    items_sold_end_index=items_sold_rcpt_cash_count-1
    # print(items_sold_rcpt_cash_values)

    items_startindex=items_sold_rcpt_cash_values[0][0]

    items_endindex=items_sold_rcpt_cash_values[items_sold_end_index][0]

    total_cost_items=0
    cash_amt=0
    upi_amt=0

    for k,v,csh,upi in items_sold_rcpt_cash_values:
        total_cost_items+=v
        cash_amt+=csh
        upi_amt+=upi


    # print(items_startindex,items_endindex,items_sold_rcpt_cash_count,total_cost_items)
    
    items_data_list=[(items_startindex,items_endindex),items_sold_rcpt_cash_count,total_cost_items,cash_amt,upi_amt]
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

    gc_cash_values=gc_cash.values_list("Receipt_Number","Date","Total_Amount","Cash","UPI")

    gc_end_index=gc_cash_count-1

    gc_start_rcpt=gc_cash_values[0][0]
    gc_end_rcpt=gc_cash_values[gc_end_index][0]

    total_cost_gc=0
    cash_amt=0
    upi_amt=0

    for k,v,amt,csh,upi in gc_cash_values:
        total_cost_gc+=amt
        cash_amt+=csh
        upi_amt+=upi
    # print(gc_start_rcpt,gc_end_rcpt,gc_cash_count,total_cost_gc)
    gc_list=[(gc_start_rcpt,gc_end_rcpt),gc_cash_count,total_cost_gc,cash_amt,upi_amt]    
    return gc_list

def exp_fun(from_date,to_date,grand_total):
    try:
        exp_data=Expenses.objects.all().filter(Date__range=(from_date,to_date))
        if not exp_data.exists():
            return grand_total,None,None
    except:
        exp_data=Expenses.objects.all().filter(Date=from_date)
        if not exp_data.exists():
            return grand_total,None,None

    exp_values=exp_data.values_list("Description","Amount")
    exp_grand_total=0

    for k,v in exp_values:
        exp_grand_total+=v
        # print(k,v)

    net_balance=grand_total-exp_grand_total
    return net_balance,exp_values,exp_grand_total

def daily_fun(net_balance):
    income_col=None
    date_col=None
    last_row=Daily_Expense.objects.last()
    income_col=last_row.Income
    date_col=last_row.Date
    
    prsent=datetime.now()
    pr_date=prsent.date()
  
    # print("############my_income", income_col,date_col,prsent,pr_date)

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
        return [],[]
    print("Donation Available")
    db_values=fetch_data.values_list("Receipt_Number","Amount_Paid","Cash","UPI")
    db_count=fetch_data.count()
    db_end_index=db_count-1
    total_donation=0
    start_index=db_values[0][0]
    end_index=db_values[db_end_index][0]
    cash_total=0
    upi_total=0
    for rc,amt,csh,upi in db_values:
        total_donation+=amt
        cash_total+=csh
        upi_total+=upi

    print(total_donation)
    donation_list=[(start_index,end_index),db_count,total_donation,cash_total,upi_total]
    return donation_list,db_values
   


def fetch_index(list_of_lists):
    
    if list_of_lists==[]:
        return 0,0,0
    else:
        return list_of_lists[2],list_of_lists[3],list_of_lists[4]

