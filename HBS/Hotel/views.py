from decimal import Decimal
from io import BytesIO
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from HBS import settings
from django.conf import settings
from django.template.loader import render_to_string
import weasyprint
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm,bookingform,searchform,roomform
from .functions import available_rooms,numberOfDays,remainig_days,calculate_days
from .models import room,booking,User,cancellation_info
from django import forms
import stripe
import datetime
from django.contrib import messages
import random
from datetime import date
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION
# check for the available rooms from checkin and checkout date
@login_required
def available_rooms_searching(request,year,month,day,year2,month2,day2):
        if request.method == "POST":
            if 'search' in request.POST:
                return redirect("Hotel:room_details")
            elif 'submit' in request.POST:
                print('submit in the request')
                room_no = request.POST.get('submit')
                start_date=(str)((str)(year)+"-"+(str)(month)+"-"+(str)(day))
                end_date=(str)((str)(year2)+"-"+(str)(month2)+"-"+(str)(day2))
                check_in_form = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
                check_out_form = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
                selected_room =room.objects.filter(room_no=room_no)
                amount = 0
                year = (check_out_form).year - (check_in_form).year
                month = (check_out_form).month - (check_in_form).month
                days = 0
                if month == 0 and year == 0:
                    days = (check_out_form).day - (check_in_form).day+1
                elif year == 0 :
                    month_days = numberOfDays((check_in_form).year,(check_in_form).month)
                    month_days2 =numberOfDays((check_out_form).year,(check_out_form).month)
                    days = month_days-(int)((check_in_form).day)+(int)((check_out_form).day)+1
                else:
                    days = remainig_days(check_in_form.year,check_in_form.month,check_in_form.day)+calculate_days(check_out_form.year,check_out_form.month,check_out_form.day)
                    print(days)
                for ro in selected_room:
                    selected_room=ro
                    amount = ro.current_price_pernight*days
                print(amount)
                check_in_form = check_in_form.strftime("%Y-%m-%d")
                check_out_form = check_out_form.strftime("%Y-%m-%d")
                print(check_in_form)
                return render(request,'payment/process.html',{'checkin':check_in_form,'checkout':check_out_form,'room':selected_room,'amount':amount,'section':'book_a_room'})
        start_date=(str)((str)(year)+"-"+(str)(month)+"-"+(str)(day))
        end_date=(str)((str)(year2)+"-"+(str)(month2)+"-"+(str)(day2))
        check_in_form = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
        check_out_form = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
        rooms = available_rooms(check_in_form=check_in_form,check_out_form=check_out_form)
        check = True
        print("hello i am back")
        check_in_form = check_in_form.strftime("%Y-%m-%d")
        check_out_form = check_out_form.strftime("%Y-%m-%d")
        print(check_in_form)
        return render(request,'Hotel/booking.html',{'rooms':rooms,'check_in':check_in_form,'check_out':check_out_form,'check':check,'section':'book_a_room'})
        # else:

        #     return HttpResponse("error")

        
        
def register(request):
    if request.user.is_authenticated:
        return render(request,"Hotel/dashboard.html",{'section':'dashboard'})
    else:
        if request.method == 'POST':
            if 'signup' in request.POST:
                user_form = UserRegistrationForm(request.POST)
                if user_form.is_valid():
                    new_user = user_form.save(commit=False)
                    new_user.set_password(user_form.cleaned_data['password'])
                    email = user_form.cleaned_data['email']
                    print(email)
                    otp = random.randint(111111,999999)
                    send_mail(
                        'Verifiction Mail For The Registration',
                        'This is a verification code for the registeration : '+(str)(otp),
                        'go229732@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    request.session['rotp']=otp
                    request.session['us']=new_user.username
                    request.session['fn']=new_user.first_name
                    request.session['ln']=new_user.last_name
                    request.session['e']=new_user.email
                    request.session['p']=new_user.password
                    # new_user.save()
                    check = True
                    return render(request,'Hotel/register_done.html',{'new_user':user_form,'check':check})
                else:
                    return render(request,'Hotel/register.html',{'user_form':user_form})
            elif 'veri' in request.POST:
                otp1 = request.POST.get('code')
                otp2 = request.session.get('rotp')
                new_user = request.POST.get('new_user')
                us = request.session.get('us')
                fn = request.session.get('fn')
                ln = request.session.get('ln')
                e = request.session.get('e')
                p = request.session.get('p')
                new_user=User(username = us,first_name = fn,last_name = ln,email=e,password=p)
                print(new_user)
                if((int)(otp1)==(int)(otp2)):
                    # print(new_user.username)
                    new_user.save()
                    return render(request,'Hotel/register_done.html')
                else:
                    check = True    
                    g= True 
                    return render(request,'Hotel/register_done.html',{'error':g,'check':check})
        else:
            user_form = UserRegistrationForm()
            return render(request,'Hotel/register.html',{'user_form':user_form})


@login_required
def dashboard(request):
    return render(request,"Hotel/dashboard.html",{'section':'dashboard'})

@login_required
def room_details(request):
    if request.method == 'POST':
            form = searchform(request.POST)
            if form.is_valid():
                check_in_form =  request.POST.get('checkin')
                check_out_form = request.POST.get('checkout')
                check_in_form = datetime.datetime.strptime(check_in_form,"%Y-%m-%d").date()
                check_out_form = datetime.datetime.strptime(check_out_form,"%Y-%m-%d").date()
                check_inyear=check_in_form.year
                check_inmonth = check_in_form.month
                check_inday = check_in_form.day
                check_outyear = check_out_form.year
                check_outmonth = check_out_form.month
                check_outday = check_out_form.day
                if check_in_form >=check_out_form:
                    error = "Atleast one day ofobooking is required"
                    if check_in_form>check_out_form:
                        error = "check in date must be less than the check out date"
                    return render(request,'Hotel/booking.html',{'form':form,'error':error,'section':'book_a_room'})
                elif check_in_form<date.today():
                    error = "Enter the proper checkin date"
                    return render(request,'Hotel/booking.html',{'form':form,'error':error,'section':'book_a_room'})
                url = form.get_url(check_inyear,check_inmonth,check_inday,check_outyear,check_outmonth,check_outday)
                print(url)
                return redirect(url)
            else:
                return render(request,'Hotel/booking.html',{'form':form})
    else:
        form = searchform()
        return render(request,'Hotel/booking.html',{'form':form,'section':'book_a_room'})
    
@login_required
def booking_form(request):
    if request.method == 'POST':
        form = bookingform(request.POST)
        if form.is_valid():
            check_in = request.POST.get('check_in')
            croom_no = request.POST.get('Room_no')
            ccheck_out = request.POST.get('check_out')
            ctotal_price = request.POST.get('total_price')
            cusername = request.POST.get('username')
            check_in = datetime.datetime.strptime(check_in,'%Y-%m-%d')
            ccheck_out = datetime.datetime.strptime(ccheck_out,'%Y-%m-%d')
            available = available_rooms(check_in_form=check_in,check_out_form=ccheck_out)
            croom_no = room.objects.get(room_no=croom_no)
            if croom_no in available:
                print("hello i am in booking form")
                croom_no.is_boocked = True
                print(croom_no.is_boocked)
                user = User.objects.get(username = cusername)
                new_booking = booking(gauest_username=user,room_no=croom_no,check_in=check_in,check_out=ccheck_out,total_price=ctotal_price)
                #payment process
                request.session['booking_room_no']=new_booking.room_no.room_no
                request.session['booking_check_in']=(str)(new_booking.check_in)
                request.session['booking_check_out']=(str)(new_booking.check_out)
                request.session['booking_total_price']=new_booking.total_price
                booking_object=new_booking
                success_url = request.build_absolute_uri(reverse('Hotel:completed'))
                cancel_url = request.build_absolute_uri(reverse('Hotel:canceled'))
                session_data={
                    'customer_email':new_booking.gauest_username.email,
                    'mode':'payment',
                    'client_reference_id':booking.id,
                    'success_url':success_url,
                    'cancel_url':cancel_url,
                    'line_items':[]
                }
                session_data['line_items'].append({
                    'price_data':{
                        'unit_amount':int((int)(ctotal_price)*Decimal('100')),
                        'currency':'inr',
                        'product_data':{
                            'name':"You Had Booked Room With Room No "+(str)(croom_no)+"",
                        },
                    },
                    'quantity':1,
                })
                session = stripe.checkout.Session.create(**session_data)
                return redirect(session.url,code=303)
                # return render(request,'Hotel/booking_conformation.html',{'section':'book_a_room'})
            else:
                return render(request,'Hotel/alreadybooked.html',{'section':'book_a_room'})
    else:
        return HttpResponse("error")


                    
@login_required
def showbookings(request):
    name = request.user.username
    print(name)
    user = User.objects.get(username = name)
    ro = room.objects.all()
    info = booking.objects.filter(gauest_username = user).order_by('room_no')
    return render(request,'Hotel/showbookings.html',{'info':info})

@login_required
def payment_completed(request):
    croom_no = request.session.get('booking_room_no')
    check_in = request.session.get('booking_check_in')
    ccheck_out = request.session.get('booking_check_out')
    ctotal_price = request.session.get('booking_total_price')
    cusername = request.user.username
    check_in = datetime.datetime.strptime(check_in,"%Y-%m-%d %H:%M:%S").date()
    ccheck_out = datetime.datetime.strptime(ccheck_out,"%Y-%m-%d %H:%M:%S").date()
    user = User.objects.get(username = cusername)
    croom_no= room.objects.get(room_no=croom_no)
    new_booking = booking(gauest_username=user,room_no=croom_no,check_in=check_in,check_out=ccheck_out,total_price=ctotal_price)
    new_booking.save()  

    #email setup for the sending mail to the user
    subject = f'Pride Plaza Hotel - Invoice no. {new_booking.id}'
    message = 'Please, find attached the invoice for your booking.'
    email = EmailMessage(subject,message,'go229732@gmail.com',[new_booking.gauest_username.email])
    html = render_to_string('payment/pdf.html',{'booking':new_booking})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    email.attach(f'Booking_{new_booking.id}.pdf',out.getvalue(),'application/pdf')
    email.send(fail_silently=False)
    return render(request,'payment/completed.html',{'section':'book_a_room'})

@login_required
def payment_canceled(request):
    return render(request,'payment/canceled.html',{'section':'book_a_room'})
        
@login_required
def aboutus(request):
    return render(request,'Hotel/aboutus.html',{'section':'about_us'})



@login_required
def cancelbooking(request,id):
    try:
        book = booking.objects.get(id = id)
    except:
        return render(request,'Hotel/alreadydeleted.html',{'section':'book_a_room'})
    
    if book:
        user1 = User.objects.get(username=book.gauest_username)
        room1 = room.objects.get(id=book.room_no.id)
        cancel= cancellation_info(gauest_username=user1,room_no=room1,check_in=book.check_in,check_out=book.check_out,total_price=book.total_price)
        cancel.save()
        print(cancel)
        booki = booking.objects.get(id=book.id)
        booki.delete()
        return render(request,'Hotel/cancelation.html',{'booking':cancel})
    
        
@login_required
def editprofile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    email = user.email
    first = user.first_name
    last = user.last_name
    if request.method == 'POST': 
        if 'verify' not in request.POST:
            username = request.POST.get('username')
            first = request.POST.get('first_name')
            last = request.POST.get('last_name')
            email = request.POST.get('email')
            use1 = User.objects.filter(email =email).exclude(username=request.user.username)
            use = User.objects.filter(username= username).exclude(username = request.user.username)
            print(use)
            use.exclude(username=request.user.username)
            use1.exclude(username=request.user.username)
            print(use)
            if use:
                print(use)
                error="user with this username already exists pls try another username"
                return render(request,'Hotel/editprofile.html',{'error':error,'username':username,'email':email,'first':first,'last':last})
            elif use1:
                error="user with this email already exists pls try another email"
                return render(request,'Hotel/editprofile.html',{'error':error,'username':username,'email':email,'first':first,'last':last})
            otp = random.randint(111111,999999)
            request.session['otp']=otp
            request.session['username']=username
            request.session['first_name']=first
            request.session['last_name']=last
            request.session['email']=email
            send_mail(
                'Verifiction Mail For The Profile Update',
                'Hello, '+username+' , This is a verification code for the updating your profile : '+(str)(otp),
                'go229732@gmail.com',
                [email],
                fail_silently=False,
            )
            return render(request,'Hotel/profileverification.html',{'otp':otp})
        elif 'verify' in request.POST:
            otp2 = request.session.get('otp')
            username = request.session.get('username')
            first = request.session.get('first_name')
            last = request.session.get('last_name')
            email = request.session.get('email')
            user1 = request.user
            user1.username = username
            user1.last_name = last
            user1.first_name = first
            user1.email = email
            otp1 = request.POST.get('code')
            if (int)(otp1) == (int)(otp2):
                user1.save()
                return render(request,'Hotel/profileverification.html',{'verified':True})
            return render(request,'Hotel/profileverification.html',{'error':True})
    else:
        return render(request,'Hotel/editprofile.html',{'username':username,'email':email,'first':first,'last':last})


def invoice(request,id):
    # bo_id = request.POST.get('print')
    book = booking.objects.get(id = id)
    html = render_to_string('payment/pdf.html',{'booking':book})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=Booking_{book.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response



@login_required
def contact(request):
    if request.method == 'POST':
        email = request.user.email
        messege = request.POST.get('message')
        print(email)
        send_mail(
                'New Contact from the '+request.user.username,
                'This messege you had received : '+(str)(messege)+' from '+(email),
                'go229732@gmail.com',
                ['kapilbhaigohil@gmail.com'],
                fail_silently=False,
            )
        return render(request,'Hotel/contact.html',{'done':True,'section':'contact'})
    return render(request,'Hotel/contact.html',{'section':'contact','email':request.user.email})

@login_required
def gallery(request):
    return render(request,'Hotel/gallery.html',{'section':'gallery'})

def printcancel(request,id):
    cn = cancellation_info.objects.get(id=id)
    html = render_to_string('Hotel/cancelationinfo.html',{'booking':cn})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=Booking_{cn.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response

def cancellation(request):
    canceldata = cancellation_info.objects.filter(gauest_username=request.user)
    print(canceldata)
    return render(request,'Hotel/cancelledbooking.html',{'info':canceldata})