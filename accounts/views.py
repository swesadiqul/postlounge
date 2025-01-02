from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from accounts.utils import *
from django.utils.timezone import now, timedelta


# Create your views here.
class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    @swagger_auto_schema(request_body=RegistrationSerializer, tags=["Authentication"], operation_id="register")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            name = serializer.validated_data.get('name')
            user = serializer.save()
            user.otp = send_email([email], name)
            user.otp_expiry = now() + timedelta(minutes=1)
            user.save()
            return Response({"status": "success", "message": "User registered successfully.", "success_code": status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPView(APIView):
    serializer_class = SendOTPSerializer
    @swagger_auto_schema(request_body=SendOTPSerializer, tags=["Authentication"], operation_id="otp")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            user.otp = send_email([email], user.name)
            user.otp_expiry = now() + timedelta(minutes=1)
            user.save()
            return Response({"status": "success", "message": "OTP sent successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid email.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    serializer_class = VerifyOTPSerializer
    @swagger_auto_schema(request_body=VerifyOTPSerializer, tags=["Authentication"], operation_id="verify-otp")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            user = User.objects.get(email=email)
            # Verify OTP
            if user.otp == otp:
                if user.otp_expiry and now() > user.otp_expiry:
                    return Response({"status": "error", "message": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({"status": "success", "message": "OTP verified successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            
            return Response({"status": "error", "message": "Invalid OTP.", "error_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = EmailVerifySerializer

    @swagger_auto_schema(request_body=EmailVerifySerializer, tags=["Authentication"], operation_id="email-verification")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): 
            user = request.user
            if user.email_verified:
                return Response({"status": "success", "message": "Email is already verified.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            user.email_verified = True
            user.save()
        return Response({"status": "success", "message": "Email verified successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, tags=["Authentication"], operation_id="login")
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            tokens = get_tokens_for_user(user)
            user.last_login = now()
            user.save()
            return Response({"status": "success", "message": "User logged in successfully.", "success_code": status.HTTP_200_OK, "tokens": tokens}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid email or password.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = LogoutSerializer

    @swagger_auto_schema(request_body=LogoutSerializer, tags=["Authentication"], operation_id="logout")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "User logged out successfully.", "code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Token is invalid or expired.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["User"], operation_id="user-list")
    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response({"status": "success", "message": "Users retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer


    @swagger_auto_schema(tags=["User"], operation_id="user-detail")
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(user)
        return Response({"status": "success", "message": "User retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=UserSerializer, tags=["User"], operation_id="update-user")
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "User updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    @swagger_auto_schema(tags=["User"], operation_id="delete-user")
    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response({"status": "success", "message": "User deleted successfully.", "code": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(request_body=ChangePasswordSerializer, tags=["Authentication"], operation_id="change-password")
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            if not user.check_password(old_password):
                return Response({"status": "error", "message": "Invalid old password.", "error_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"status": "success", "message": "Password changed successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(request_body=PasswordResetSerializer, tags=["Authentication"], operation_id="password-reset")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            user.otp = send_email([email], user.name)
            user.otp_expiry = now() + timedelta(minutes=1)
            user.save()
            return Response({"status": "success", "message": "OTP sent successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid email.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    @swagger_auto_schema(request_body=PasswordResetConfirmSerializer, tags=["Authentication"], operation_id="password-reset-confirm")
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            new_password = serializer.validated_data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({"status": "success", "message": "Password reset successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)