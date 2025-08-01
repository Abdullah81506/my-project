from rest_framework import serializers
from .models import Post, Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.utils.text import slugify

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Profile
        fields = ['id', 'user', 'bio', 'profile_img', 'slug']

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label="Confirm Password")
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_img = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio', 'profile_img']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        bio = validated_data.pop('bio', '')
        profile_img = validated_data.pop('profile_img', None)

        # Create the user
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create the profile
        Profile.objects.create(
            user=user,
            bio=bio,
            profile_img=profile_img,
            slug=slugify(user.username)
        )

        return user