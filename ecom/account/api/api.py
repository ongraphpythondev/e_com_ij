from rest_framework import permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView

from .serializers import (CreateUserSerializer, 
                          UserSerializer, LoginUserSerializer)
from account.models import User, PhoneOTP
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from account.utils import otp_generator

class SendOTP(APIView):
    def post(self,request):
        print(request.data)
        phone_number = request.data.get('phone')
        if not phone_number:
            return Response({'phone_no':'required'})
        saved_otp = PhoneOTP.objects.filter(phone=phone_number).first()
        otp = otp_generator()
        print(otp)
        if saved_otp:
            saved_otp.otp = otp
            saved_otp.save()
        else:
            new_otp_instance = PhoneOTP(phone=phone_number,otp=otp)
            new_otp_instance.save()

        return Response({'status': True, 'otp':'Kindly validate sent OTP'})

class Registeration(APIView):
    
    def post(self,request):
        if request.user.is_authenticated:
            return Response({ 'status': False, 'message':'Logged In'})
        phone_no = request.data.get('phone')
        otp = request.data.get('otp')
        user = User.objects.filter(phone=phone_no).first()
        if user:
            return Response({ 'status': False, 'message':'Phone Number already exists'})
       # print(phone_no)
        otp_object = PhoneOTP.objects.filter(phone=phone_no).first()
        print(request.data)
        Temp_data = {'phone': phone_no, 'password': 'a' }
        if not otp_object:
            return Response({ 'status': False, 'message': 'Please get an otp on your number first'})
        serializer = CreateUserSerializer(data=Temp_data)
       # print(serializer)
        if serializer.is_valid():
            print("valid")
            if int(otp) != otp_object.otp:
                return Response({'status': False, 'message': 'Please enter correct OTP'})
            user = serializer.save()
            login(request,user)
            PhoneOTP.objects.filter(phone=phone_no).delete()
            return Response({"success":f"{phone_no} is registered successfully and logged in"})
        return Response(serializer.errors)





class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.last_login is None :
            user.first_login = True
            user.save()
            
        elif user.first_login:
            user.first_login = False
            user.save()
            
        login(request, user)
        
        return super().post(request, format=None)

class UserAPI(generics.RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



