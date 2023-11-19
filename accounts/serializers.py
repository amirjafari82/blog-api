from rest_framework import serializers
from accounts.models import User, Profile
from rest_framework.exceptions import AuthenticationFailed


class UserRegisterSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(required=True,write_only=True)
    
    class Meta:
        model = User
        fields = ('phone','first_name','last_name','password','password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)
    
    def validate_phone(self, value):
        if not value.startswith('09'):
            raise serializers.ValidationError('Phone Number Must Start with 09')
        if len(value) < 11:
            raise serializers.ValidationError('Phone Number Must Be 11 numbers')
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password Must Match!')
        return data
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('phone','password')
        
    def validate(self, data):
        user = User.objects.filter(phone=data['phone']).first()
        if not user.exists():
            raise AuthenticationFailed('User Not Found!')
        if not user.check_password(data['password']):
            raise AuthenticationFailed('Incorrect Password!')
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ('bio','age')