from django.contrib import admin
from .models import room,booking
# Register your models here.

@admin.register(room)
class roomAdmin(admin.ModelAdmin):
    list_display=['room_no','room_type','is_boocked','room_image']
    list_filter = ['room_type']
    search_fields = ['room_no']
    ordering =['room_no','room_type']

@admin.register(booking)
class bookingAdmin(admin.ModelAdmin):
    list_display =['room_no','check_in','check_out','total_price','created']


