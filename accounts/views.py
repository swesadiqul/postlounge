from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from accounts.serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema



# Create your views here.
class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer, tags=["Authentication"], operation_id="register")
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "User registered successfully.", "success_code": status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Invalid input data.", "error_code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     @swagger_auto_schema(request_body=LoginSerializer, tags=["Authentication"], operation_id="login")
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             tokens = get_tokens_for_user(request.user)
#             return Response({"status": "success", "message": "User logged in successfully.", "code": status.HTTP_200_OK, "tokens": tokens}, status=status.HTTP_200_OK)
#         return Response({"status": "error", "message": "Invalid email or password.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     serializer_class = LogoutSerializer

#     @swagger_auto_schema(request_body=LogoutSerializer, tags=["Authentication"], operation_id="logout")
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "message": "User logged out successfully.", "code": status.HTTP_200_OK}, status=status.HTTP_200_OK)
#         return Response({"status": "error", "message": "Token is invalid or expired.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    


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
    

