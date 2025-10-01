from django import forms
from .models import Comment, Subscribe, Post, Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'Type Your Comment...'


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']
        labels = {'email': _('')} #this will reset the label and we can add placeholder of our own choice 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'

class NewForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_img = forms.ImageField(required=False) # false because this field is kept optional.
    class Meta:
        model=User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_img') # built-in fields of user model also custom fields fetched created above

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['profile_img'].widget.attrs['placeholder'] = 'Profile Image (Optional)'


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email
    
    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords dont match')
        return password2
    
class CreatePostForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        help_text="Enter new tags separated by commas",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. django, ai, blog'})
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags', 'is_featured']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(), # this tells django to render tags field using checkboxes instead of default multi-selsct dropdown
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_img', 'bio']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

        