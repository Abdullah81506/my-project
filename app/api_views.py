from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import Post, Profile
from .serializers import PostSerializer, ProfileSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAuthorReadOnly, IsOwner
from rest_framework import viewsets
from django.contrib.auth.models import User

class PostLCAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] # this means only logged in users can use this view

    def perform_create(self, serializer): # Automatically sets the author to the current logged in user.
        serializer.save(author=self.request.user)

class PostRUPAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsAuthorReadOnly] #this means the same as above but one addition is that this view that handles update, delete can only be done by author

    def get_object(self):
        # Return only the profile of the currently authenticated user
        return Profile.objects.get(user=self.request.user)

class ProfileRUPAPIView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Users can only view/edit their own profile
        return Profile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]