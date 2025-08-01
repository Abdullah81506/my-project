from django.shortcuts import render, redirect, get_object_or_404
from app.models import Post, Comment, Tag, Profile, WebsiteMeta, Subscribe
from .forms import CommentForm, SubscribeForm, NewForm, CreatePostForm , UserEditForm, ProfileEditForm 
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.

def index(request):
    post = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured=True)

    if featured_blog:
        featured_blog = featured_blog[0]

    context = {
        'posts': post, 'top_post': top_post, 'recent_post': recent_post,
        'featured_blog': featured_blog
    }
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comment_count = Comment.objects.filter(post=post).count()
    comments = Comment.objects.filter(post=post, parent=None)
    form = CommentForm() # instance of the form is created

    # Bookmark logic to show if user has already bookmarked or not when the post page is opened
    bookmarked = False
    if post.bookmark.filter(id=request.user.id).exists(): #checks if the post is bookmarked by the user or not.
        bookmarked = True 
    is_bookmarked = bookmarked

    # Likes logic to show if user has already liked or not when post page is opened
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes
    is_liked = liked

    #sidebar 
    recent_posts = Post.objects.exclude(id=post.id).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')
    tags = Tag.objects.all()
    related_posts = Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]

    if request.POST:
        if not request.user.is_authenticated: # if user is not verified will be redirected to login
            return redirect('login') 
        comment_form = CommentForm(request.POST) 
        if comment_form.is_valid():
            parent_obj = None
            # condition to save as replies or comments
            if request.POST.get('parent'): # if request is from reply form (parent specifies that form) saved as reply
                parent = request.POST.get('parent')
                parent_obj = Comment.objects.get(id=parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.author = request.user # sets user to author
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug})) #slug was passed in url and parameters are passed using kwargs
            else: # save as comment
                comment = comment_form.save(commit=False) 
                postid = request.POST.get('post_id') 
                post = Post.objects.get(id=postid)
                comment.post = post
                comment.author = request.user
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug})) #slug was passed in url and parameters are passed using kwargs

    # recording views only once per session per post
    viewed_posts = request.session.get('viewed_posts', [])
    if post.id not in viewed_posts:
        if post.view_count is None: #for recording views
            post.view_count = 1
        else:
            post.view_count += 1 
        post.save()
        viewed_posts.append(post.id)
        request.session['viewed_posts'] = viewed_posts

    context = {
        'post': post, 'form': form, 'comments': comments, 'is_bookmarked': is_bookmarked,
        'is_liked': is_liked, 'number_of_likes': number_of_likes, 'recent_posts': recent_posts,
        'top_authors': top_authors, 'tags': tags, 'related_posts': related_posts, 'comment_count':comment_count
    } # instances is passed in the context so templates can access it using the keys in this dictionary
    return render(request, 'app/post.html', context)

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug) #specific tag from the URL
    top_post = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2] # gets all posts of the requested tag and sorts in descending order
    recent_post = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:2] 
    tags = Tag.objects.all() #list of all tags in the databse
    context = {'tag': tag, 'top_post': top_post, 'recent_post': recent_post, 'tags': tags}
    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    author = Profile.objects.get(slug=slug) #specific author from the URL
    top_post = Post.objects.filter(author=author.user).order_by('-view_count')[0:3] # gets all posts of the requested author and sorts in descending order
    recent_post = Post.objects.filter(author=author.user).order_by('-last_updated')[0:3] 
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number') #gets all users, counts their posts and sort them in descending order
    context = {'author': author, 'top_post': top_post, 'recent_post': recent_post, 'top_authors': top_authors}
    return render(request, 'author/author.html', context)

def search(request):
    search_query = ''
    if request.GET.get('q'): #checks if get request has parameter 'q' 
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query) #gets all posts where the title contains search query
    context = {'posts': posts, 'search_query': search_query}
    return render(request, 'app/search.html', context)

def about(request):
    website_info = None
    if WebsiteMeta.objects.all().exists(): #checks if the object of the model exists to avoid crash incase it doesnt exist.
        website_info = WebsiteMeta.objects.all()[0] #assigns the first object if there are more than 1 object of the model.
    context = {'website_info': website_info}
    return render(request, 'app/about.html', context)

def register_user(request):
    form = NewForm()
    if request.method == "POST": # handles post request 
        form = NewForm(request.POST, request.FILES) #.files is included to handle image upload
        if form.is_valid():
            user = form.save(commit=False) #false indicated that make an object for this user but not save it yet 
            # Save first and last name from form
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            # Handle image and slug creation
            profile_img = form.cleaned_data.get('profile_img')
            Profile.objects.create(
                user=user,
                profile_img=profile_img if profile_img else 'images/default.png',
                slug=slugify(user.username)
            )
            login(request, user) # inbuilt function that marks the user as logged in by creating or updating session cookie in browser.
            return redirect('/')
    context = {'form': form}
    return render(request, 'registration/register.html', context)

def bookmark(request, slug): #handles click action to bookmark/un-bookmark
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # fetches specific post user is trying to interact with in the form
    if post.bookmark.filter(id=request.user.id).exists(): #if post is bookmaked remove it from db else, add it in db
        post.bookmark.remove(request.user)
    else: 
        post.bookmark.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def likes(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # fetches specific post user is trying to interact with in the form
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def all_bookmarks(request):
    all_bookmarked_posts = Post.objects.filter(bookmark=request.user)
    context = {'all_bookmarked_posts': all_bookmarked_posts}
    return render(request, 'app/all_bookmarks.html', context)

def all_posts(request):
    allposts = Post.objects.all()
    context = {'allposts': allposts}
    return render(request, 'app/all_posts.html', context)

def all_likes(request):
    alllikes = Post.objects.filter(likes=request.user)
    context = {'alllikes': alllikes}
    return render(request, 'app/all_likes.html', context)


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST) #instance of form is created
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to subscribe.') # warning message is added
            return redirect('login')  # Or reverse('login') if preferred

        if form.is_valid():
            email = form.cleaned_data['email'] #email is fetched 
 
            if not Subscribe.objects.filter(email=email).exists(): #avoids duplicate emails
                subscription = form.save(commit=False)
                subscription.user = request.user  # Only reached if user is authenticated
                subscription.save()
                messages.success(request, 'Subscribed successfully!')
        else:
            # This will automatically show specific form errors (like invalid email) in the template
            messages.error(request, 'Invalid email. Please enter a valid one.')

    return redirect(request.META.get('HTTP_REFERER', '/'))  #better than redirect as this redirecs to the same page whereuser was on

def unsubscribe_view(request):
    if request.method == 'POST':
        Subscribe.objects.filter(user=request.user).delete()
        messages.success(request, 'You have successfully unsubscribed')
    return redirect(request.META.get('HTTP_REFERER', '/'))

def author_all_post(request, slug):
    author = get_object_or_404(Profile, slug=slug) #specific author from the URL
    all_posts = Post.objects.filter(author=author.user).order_by('-last_updated') # gets all posts of the requested author and sorts in newest to oldest
    context = {'author':author, 'all_posts':all_posts}
    return render(request, 'author/author_all_post.html', context)

def create_post(request, slug):
    author_profile = get_object_or_404(Profile, slug=slug)  # gets one requested author if exists
    # Block other users from accessing this page
    if request.user != author_profile.user:
        return HttpResponseForbidden("You are not allowed to create a post for this author.")

    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)  # initializes the form with data submitted by the user via post request
        if form.is_valid():
            post = form.save(commit=False)
            post.author = author_profile.user  # sets author of post to the currently logged in user
            post.slug = slugify(post.title)
            post.view_count = 0
            post.save()
            form.save_m2m()  # to save tags

            # --- Handle new_tags input if any ---
            new_tags_input = form.cleaned_data.get('new_tags')
            if new_tags_input:
                new_tags = [t.strip() for t in new_tags_input.split(',')]
                for tag_name in new_tags:
                    if tag_name:  # avoid blank tags
                        tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag_obj)
            # --- End of new_tags logic ---

            return redirect('author_all_post', slug=slug)
    else:
        form = CreatePostForm()  # shows an empty form on get request

    context = {'form': form, 'author_profile': author_profile}
    return render(request, 'app/create_post.html', context)



def edit_post(request, slug, post_id):
    post = get_object_or_404(Post, id=post_id, author__profile__slug=slug) 
     # Block other users from accessing this page
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to create a post for this author.")

    if request.method =='POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post) # instance binds the form to an existing post to indicate the post is being edited not created
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.slug = slugify(updated_post.title)
            updated_post.save()
            form.save_m2m()

             # --- Handle new_tags input if any ---
            new_tags_input = form.cleaned_data.get('new_tags')
            if new_tags_input:
                new_tags = [t.strip() for t in new_tags_input.split(',')]
                for tag_name in new_tags:
                    if tag_name:  # avoid blank tags
                        tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                        post.tags.add(tag_obj)
            # --- End of new_tags logic ---
            
            return redirect('author_all_post', slug=slug)
    else:
        form = CreatePostForm(instance=post)
    context = {'form':form, 'author_profile':post.author.profile}
    return render(request, 'app/create_post.html', context)
    

def delete_post(request, slug, post_id):
    post = get_object_or_404(Post, id=post_id, author__profile__slug=slug) 
     # Ensure only the author can delete
    if request.user != post.author:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('author_all_post', slug=slug)
    
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    post_slug = comment.post.slug  # for redirect
    comment.delete()
    return redirect('post_page', slug=post_slug)             

def edit_profile(request, slug):
    profile = request.user.profile
    user = request.user
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('author_page', slug=profile.slug)
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)
    context = { 'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'author/edit.html', context)