from .models import room,booking
from datetime import date

def available_rooms(check_in_form,check_out_form):
    rooms = room.objects.all()
    c = date.today()
    deleterec = booking.objects.all().filter(check_out__lt = c).values_list('room_no',flat=True)
    for d in deleterec:
        for r in rooms:
            if (int)(r.id) ==d:
                same = booking.objects.all().filter(room_no=d)
                if same is None:
                    r.is_boocked = False
                    r.save()
                
    booking.objects.all().filter(check_out__lt=c).delete()
    bookings = booking.objects.all().filter(check_out__gte = check_in_form,check_in__lte = check_out_form).values_list('room_no',flat=True)
    g = bookings
    for x in g:
            for r in rooms:
                # print(x)
                # print(r.id)
                if x ==(int)(r.id):
                    rooms = rooms.exclude(id = x)
    return rooms

def numberOfDays(y, m):
      leap = 0
      if y% 400 == 0:
         leap = 1
      elif y % 100 == 0:
         leap = 0
      elif y% 4 == 0:
         leap = 1
      if m==2:
         return 28 + leap
      list = [1,3,5,7,8,10,12]
      if m in list:
         return 31
      return 30

def total_days(y):
    leap = 0
    if y% 400 == 0:
         leap = 1
    elif y % 100 == 0:
         leap = 0
    elif y% 4 == 0:
         leap = 1
    return leap
def calculate_days(y,m,d):
    days = d
    for r in range(1,m):
        print(r)
        list = [1,3,5,7,8,10,12]
        if r  in list:
            days+=31
        elif r ==2:
            days+=28+total_days(y)
        else:
            days+=30
    return days

def remainig_days(y,m,d):
    if total_days(y)==1:
        year_days = 366
    else:
        year_days = 365
    days = calculate_days(y,m,d)
    return year_days - days+1

    
    

