from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from blogs.models import *
from blogs.serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404



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
    

class TagListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    @swagger_auto_schema(tags=["Tag"], operation_id="Get all tags")
    def get(self, request):
        tags = Tag.objects.all()
        serializer = self.serializer_class(tags, many=True)
        return Response({"status": "success", "message": "Tags retrieved successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
    

class TagCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    @swagger_auto_schema(request_body=TagSerializer, tags=["Tag"], operation_id="Create a tag")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Tag created successfully!", "code": status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class TagDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    @swagger_auto_schema(tags=["Tag"], operation_id="Get a tag by ID")
    def get(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"status": "error", "message": "Tag not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(tag)
        return Response({"status": "success", "message": "Tag retrieved successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
    

class TagUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer


    @swagger_auto_schema(request_body=TagSerializer, tags=["Tag"], operation_id="Update a tag")
    def put(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"status": "error", "message": "Tag not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=tag, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Tag updated successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class TagDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = TagSerializer

    @swagger_auto_schema(tags=["Tag"], operation_id="Delete a tag")
    def delete(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({"status": "error", "message": "Tag not found.", "code": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        tag.delete()
        return Response({"status": "success", "message": "Tag deleted successfully!", "code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
    

# List all posts
class PostListAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    @swagger_auto_schema(tags=["Post"], operation_id="Get all posts")
    def get(self, request):
        """
        Only show published posts.
        """
        posts = Post.objects.filter(status='published')
        serializer = self.serializer_class(posts, many=True)
        return Response({'status': 'success', 'message': 'Posts retrieved successfully!', 'code': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)


# Create a new post
class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostSerializer, tags=["Post"], operation_id="Create a post")
    def post(self, request):
        """
        Create a new post.
        The logged-in user is automatically set as the author.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"status": "success", "message": "Post created successfully!", "code": status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Retrieve a specific post
class PostRetrieveAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    @swagger_auto_schema(tags=["Post"], operation_id="Get a post by ID")
    def get(self, request, pk):
        """
        Retrieve a specific post by ID.
        """
        post = get_object_or_404(Post, pk=pk)
        # Unauthenticated users can only view published posts
        if not request.user.is_authenticated and post.status != 'published':
            return Response({"status": "success", "message": "Post not found.", "code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(post)
        return Response({"status": "success", "message": "Post retrieved successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)


# Update a specific post (full update)
class PostUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostSerializer, tags=["Post"], operation_id="Update a post")
    def put(self, request, pk):
        """
        Update a specific post (replace all fields).
        """
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"status": "error", "message": "You do not have permission to update this post.", "code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Partially update a specific post
class PostPartialUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostSerializer

    @swagger_auto_schema(request_body=PostSerializer, tags=["Post"], operation_id="Partially update a post")
    def patch(self, request, pk):
        """
        Partially update a specific post.
        """
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"status": "error", "message": "You do not have permission to update this post.", "code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Post updated successfully!", "code": status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": "Invalid input data.", "code": status.HTTP_400_BAD_REQUEST, "detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Delete a specific post
class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(tags=["Post"], operation_id="Delete a post")
    def delete(self, request, pk):
        """
        Delete a specific post.
        """
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"status": "error", "message": "You do not have permission to delete this post.", "code": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({"status": "success", "message": "Post deleted successfully.", "code": status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
