import django
from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views 
from django.urls import reverse_lazy

app_name = 'Hotel'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('password-change/',auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('Hotel:password_change_done')),name='password_change'),
    path('passwor-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password-reset/',auth_views.PasswordResetView.as_view(success_url=reverse_lazy('Hotel:password_reset_done')),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('Hotel:password_reset_complete')),name='password_reset_confirm'),
    path('password-reset/complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('register/',views.register,name='register'),
    # path('email_verification',views),
    path('room_details/',views.room_details,name='room_details'),
    path('booking_form/',views.booking_form,name='booking_form'),
    # path('booking.html/',views.room_details,name='booking')
    # path('booking_conformation.html',views.booking_confromation,name='booking_conformation'),
    path('room_details/available_rooms_searching/<int:year>/<int:month>/<int:day>/<int:year2>/<int:month2>/<int:day2>/',views.available_rooms_searching,name='available_rooms_searching'),
    path('',views.dashboard,name='dashboard'),
    path('showbookings',views.showbookings,name='showbookings'),
    path('completed/', views.payment_completed, name='completed'),
    path('canceled/', views.payment_canceled, name='canceled'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contact',views.contact,name='contact'),
    path('cancelbooking/<int:id>',views.cancelbooking,name='cancelbooking'),
    # path('webhook/',views.my_webhook_view,name='webhook'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('invoice/<int:id>',views.invoice,name='invoice'),
    path('gallary',views.gallery,name="gallery"),
    path('printcancel/<int:id>',views.printcancel,name="printcancel"),
    path('cancellation/',views.cancellation,name='cancellation'),
]