from lib2to3.pgen2 import token
from django.forms import ValidationError
from rest_framework import serializers
from Auth.models import CustomUser
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import AnonymousUser



# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('id', 'email', 'first_name', 'last_name', 'city')

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'city', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user



class UserLoginSerializer(serializers.ModelSerializer):

    email=serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email','first_name','last_name','is_active','is_staff','password']    

    def get_email(self, obj):
        print('=========obj=========',obj)
        if isinstance(obj, AnonymousUser):
            return None
        return obj.email      


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password2'},write_only=True)
    class Meta:
        model = CustomUser
        fields=['password','password2']
    
    def validate(self,attrs):
        print('======attrs========',attrs)
        password = attrs.get('password')
        password2 = attrs.get('password2')

        user = self.context.get('user')  # this user value get from views.py line no : 80 
 
        print('=========user=====',user)
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match.')
        user.set_password(password)
        user.save()
        return attrs      
    

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = CustomUser
        fields = ['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print({'Encoded UID':uid})
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link='//http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link:',link)
            #Send email code
            print('=============attrs===========',attrs)
            return attrs
        
        else:

            raise serializers.ValidationError('You are not register user')   


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password2'},write_only=True)
    class Meta:
        model = CustomUser
        fields=['password','password2']
    
    def validate(self,attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password and Confirm Password does not match.')
            id=smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
                PasswordResetTokenGenerator().check_token(user,token)  
                raise ValidationError('Token is not valid or Expired')          