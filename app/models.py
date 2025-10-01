from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import os
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(blank=True, upload_to="images/", default='images/default.png',)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args, **kwargs): #this will automatically generate a slug when profile will be created.
        if not self.slug:  # this checks if slug is empty (not just id)
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs) # cleaner than  return super(Profile, self).save(*args, **kwargs)

    def __str__(self): #for admin panel
        return self.user.username


class Subscribe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self): # for admin panel
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs): #this will automatically generate a slug when tag will be created.
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)
    
    def __str__(self): #for admin panel
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')  #related_name is used to get post of a particular tag just like using post.tags.all() to get all tags for a post.
    view_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bookmark = models.ManyToManyField(User, related_name='bookmark', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def number_of_likes(self):
        return self.likes.count()
    
    def delete(self, *args, **kwargs):
        # Avoid deleting default.jpg
       def delete(self, *args, **kwargs):
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.exists(image_path):
                os.remove(image_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model): #fields like name, email, website are removed because this model is connected to the built-in user model
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # models.CASCADE will delete the comment if post or the author is deleted from the database.
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='replies') #this field is related to itself (for replies) yaani if parent is none its a top level comment, else, reply

class WebsiteMeta(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    about = models.TextField()