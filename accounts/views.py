from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserRegisterSerializer, UserProfileSerializer, UserLoginSerializer
from accounts.models import User
from .tokens import create_jwt_pair_for_user
from django.conf import settings
from django.contrib.auth.hashers import check_password
import jwt,datetime


class UserRegister(APIView):
    
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
class LoginView(APIView):
    
    def post(self, request: Request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        user = User.objects.filter(phone=phone).first()
        if user is None:
            print(user.check_password(user.password))
            raise AuthenticationFailed('User Not Found!')
        if not check_password(password,user.password):
            raise AuthenticationFailed('Incorrect Password!')
        
        tokens = create_jwt_pair_for_user(user)
        print(tokens)
        
        return Response({'message': 'Login Successful','tokens':tokens})
    
    
class Logoout(APIView):
    
    def get(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    
    
class EditProfileView(APIView):
    
    def put(self, request):
        srz_data = UserProfileSerializer(data=request.data,partial=True)
        if srz_data.is_valid():
            srz_data.save(user=request.user)
            return Response(srz_data.data,status.HTTP_200_OK)
        return Response(srz_data.errors,status.HTTP_400_BAD_REQUEST)