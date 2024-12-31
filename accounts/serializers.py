from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



class RegisterSerializer(serializers.ModelSerializer):
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
            'id', 'email_verified', 'profile_picture', 'bio', 'social_links', 
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
    

# class LoginSerializer(serializers.ModelSerializer):
#     identifier = serializers.CharField()
#     password = serializers.CharField(write_only=True, style={'input_type': 'password'})

#     class Meta:
#         model = User
#         fields = ['email', 'password']


#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')

#         # Check if the user exists
#         if not User.objects.filter(email=email).exists():
#             raise ValidationError({"email": "User not found."})

#         # Check if the password is correct
#         user = User.objects.get(email=email || username=email)
#         if not user.check_password(password):
#             raise ValidationError({"password": "Incorrect password."})
#         return attrs

   
# class LogoutSerializer(serializers.Serializer):
#     refresh_token = serializers.CharField()

#     def validate(self, attrs):
#         refresh_token = attrs.get('refresh_token')

#         # Check if the refresh token is provided
#         if not refresh_token:
#             raise ValidationError({"refresh_token": "Refresh token is required."})
        
#         try:
#             RefreshToken(refresh_token)
#         except TokenError:  # Catch invalid or expired tokens
#             raise ValidationError({"refresh_token": "Token is invalid or expired."})
        
#         return attrs

        
    # def save(self, **kwargs):
    #     # Blacklist the refresh token
    #     RefreshToken(self.validated_data['refresh_token']).blacklist()
    #     return True
    


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()

#     class Meta:
#         fields = ['username', 'password']
    
#     def validate(self, data):
#         username = data.get('username', None)
#         password = data.get('password', None)
#         if username is None:
#             raise ValidationError("identifier": "Username is required.")
#         if password is None:
#             raise ValidationError("Password is required.")
#         return data
    


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


