from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
    @swagger_auto_schema(request_body=VerifyOTPSerializer, tags=["Authentication"], operation_id="verify-otp")
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            user = User.objects.get(email=email)
            # Verify OTP
            if user.otp == otp:
                if user.otp_expiry and now() > user.otp_expiry:
                    return Response({"status": "error", "message": "OTP has expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # OTP is valid
                user.email_verified = True
                user.otp = None
                user.otp_expiry = None
                user.save()
                return Response({"status": "success", "message": "Email verified successfully.", "success_code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
            return Response({"status": "error", "message": "Invalid OTP.", "error_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer, tags=["Authentication"], operation_id="login")
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            tokens = get_tokens_for_user(user)
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



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer

    @swagger_auto_schema(tags=["User"], operation_id="profile")
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({"status": "success", "message": "User profile retrieved successfully.", "data": serializer.data}, status=status.HTTP_200_OK)



# class UserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#     def get(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#     def delete(self, request, pk):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

