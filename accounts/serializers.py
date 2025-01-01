from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'password', 'confirm_password', 
            'phone_number', 'address', 'email_verified', 'profile_picture', 
            'bio', 'social_links', 'role', 'terms_accepted', 
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = [
            'id', 'phone_number', 'address', 'email_verified', 'profile_picture', 'bio', 'social_links', 
            'role', 'terms_accepted', 'created_at', 'updated_at', 'last_login'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({"confirm_password": "Password doesn't match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']
    
    def validate_email(self, email):
        email = email.lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError("The provided email does not exist.")
        return email
    

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        fields = ['email', 'otp']
    
    def validate_email(self, email):
        email = email.lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError("The provided email does not exist.")
        return email
    
    def validate(self, data):
        email = data.get('email').lower()
        otp = data.get('otp')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({"email": "User does not exist."})

        # Check if the OTP matches
        if user.otp != otp:
            raise ValidationError({"otp": "Invalid OTP."})

        # Check if OTP is expired
        if user.otp_expiry and now() > user.otp_expiry:
            raise ValidationError({"otp": "OTP has expired. Please request a new one."})

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise ValidationError({"email": "Email is required."})
        if not password:
            raise ValidationError({"password": "Password is required."})

        # Use Django's authenticate function
        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise ValidationError({"message": "Invalid email or password."})
        
        # If authentication is successful, add user to the validated data
        data['user'] = user
        return data
    


   
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')

        # Check if the refresh token is provided
        if not refresh_token:
            raise ValidationError({"refresh_token": "Refresh token is required."})
        
        try:
            RefreshToken(refresh_token)
        except TokenError:  # Catch invalid or expired tokens
            raise ValidationError({"refresh_token": "Token is invalid or expired."})
        
        return attrs

        
    def save(self, **kwargs):
        # Blacklist the refresh token
        RefreshToken(self.validated_data['refresh_token']).blacklist()
        return True
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone_number', 'address', 'email_verified', 'profile_picture', 'bio', 'social_links', 'role', 'is_active', 'is_staff', 'is_superuser', 'terms_accepted', 'created_at', 'updated_at', 'last_login']
        


    

# class UserUpdateSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=False)
#     confirm_password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password', 'confirm_password', 'phone_number', 'address', 'email_verified', 'profile_picture', 'bio', 'social_links', 'location', 'role', 'is_active', 'is_staff', 'is_superuser', 'terms_accepted', 'created_at', 'updated_at', 'last_login']
#         read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']


#     def validate(self, data):
#         if 'password' in data:
#             if data['password'] != data['confirm_password']:
#                 raise ValidationError("Passwords do not match.")
#             validate_password(data['password'])
#         return data
    
#     def update(self, instance, validated_data):
#         if 'password' in validated_data:
#             validated_data.pop('confirm_password')
#             instance.set_password(validated_data['password'])
#         instance.save()
#         return instance
    


# class UserListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'email_verified', 'created_at', 'updated_at', 'last_login']
#         read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
    



# class UserDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'phone_number', 'address', 'email_verified', 'profile_picture', 'bio', 'social_links', 'location', 'role', 'is_active', 'is_staff', 'is_superuser', 'terms_accepted', 'created_at', 'updated_at', 'last_login']
#         read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']


