from typing import Iterable
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

# Create your models here.
class room(models.Model):
    class Type(models.TextChoices):
        King_Size_Four_Poster = "King Size Four Poster"
        King_Size_Sleigh_Bed = "King Size Sleigh Bed"
        Deluxe_King_Size = "Deluxe King Size"
        Deluxe_Twin_Large_Double = "Deluxe Twin/Large Double"
        Compact_Double = "Compact Double"
        Family_Room ="Family Room"
        Single = "Single"
    room_image = models.ImageField(upload_to='static/images')
    room_no = models.CharField(max_length=4,unique=True)
    room_description = models.TextField()
    room_type = models.CharField(max_length=24,choices=Type.choices,default=Type.Single)
    beds = models.IntegerField(default=1)
    capasity = models.IntegerField(default=2)
    current_price_pernight = models.IntegerField(default=800)
    is_boocked = models.BooleanField(default=False)

    def __str__(self):
        return self.room_no
    
    def get_url(self):
        return reverse("Hotel:booking_form",args=[self.room_no])
    
class booking(models.Model):
    gauest_username = models.ForeignKey(User,on_delete=models.CASCADE)
    room_no = models.ForeignKey(room,on_delete=models.CASCADE)
    check_in = models.DateField(null=True,default=None)
    check_out = models.DateField(null=True,default=None)
    total_price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.gauest_username} has booked {self.room_no} from {self.check_in} to {self.check_out}'
    
    def url(self):
        return reverse("Hotel:cancelbooking",args=[self.id])
    def get_invoice_url(self):
        return reverse("Hotel:invoice",args=[self.id])
    
class cancellation_info(models.Model):
    gauest_username = models.ForeignKey(User,on_delete=models.CASCADE)
    room_no = models.ForeignKey(room,on_delete=models.CASCADE)
    check_in = models.DateField(null=True,default=None)
    check_out = models.DateField(null=True,default=None)
    total_price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    