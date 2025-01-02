from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from blogs.models import *
from blogs.serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication



# Create your views here.
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=["Category"], operation_id="Get all categories")
    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response({"status": "success", "message": "Categories retrieved successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
    

class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    @swagger_auto_schema(request_body=CategorySerializer, tags=["Category"], operation_id="Create a category")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Category created successfully!", "code": status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=["Category"], operation_id="Get a category by ID")
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(category)
        return Response({"status": "success", "message": "Category retrieved successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)

class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    @swagger_auto_schema(request_body=CategorySerializer, tags=["Category"], operation_id="Update a category")
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Category updated successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=["Category"], operation_id="Delete a category")
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"status": "error", "message": "Category not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({"status": "success", "message": "Category deleted successfully!", "code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
    


    
