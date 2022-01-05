
   
from django.urls import path,include
from account.api.api import  SendOTP, Registeration, LoginAPI

urlpatterns = [

    path('sendotp/',SendOTP.as_view(),name='send_otp'),
    path('register/',Registeration.as_view(),name='register'),
    path('login/', LoginAPI.as_view(), name='login')
    
]