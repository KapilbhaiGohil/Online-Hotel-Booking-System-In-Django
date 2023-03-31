from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.urls import reverse
from .models import booking,room

# class LoginForm(forms.Form):
#     Username = forms.CharField(required=True)
#     Password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password don't match.")
        return cd['password2']
    

class bookingform(forms.ModelForm):
    First_name = forms.CharField()
    Last_name = forms.CharField()
    Email = forms.EmailField()
    Room_no = forms.IntegerField()
    Room_type = forms.CharField()
    Beds = forms.IntegerField()
    Capasity = forms.IntegerField()
    class Meta:
        model = booking
        fields = ['check_in','check_out','total_price']


class searchform(forms.Form):
    checkin = forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}))
    checkout = forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}))

    def get_url(self,year,month,day,year2,month2,day2):
        return reverse("Hotel:available_rooms_searching",args=[year,month,day,year2,month2,day2])

class roomform(forms.ModelForm):
    class Meta:
        model = room
        fields = ['room_no','room_type','beds','capasity','current_price_pernight']

