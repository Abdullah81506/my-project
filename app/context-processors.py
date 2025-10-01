from .forms import SubscribeForm
from .models import WebsiteMeta, Tag, Subscribe
from django.contrib.auth.models import User
from django.db.models import Count

def global_context(request):
    website_info = WebsiteMeta.objects.first() #gets first record from the table
    tags = Tag.objects.all()
    top_authors = User.objects.annotate(number=Count('post')).order_by('-number')[0:3] # gets top 3 users by post count

    subscribe_form = SubscribeForm()
    subscribed = False

    # Check if logged-in user already subscribed
    if request.user.is_authenticated:
        subscribed = Subscribe.objects.filter(user=request.user).exists() # this line checks if user exists and if it does the boolean value will automatically turn True due to the .exists()

    return {
        'subscribe_form': subscribe_form,
        'subscribed': subscribed,
        'website_info': website_info,
        'tags': tags,
        'top_authors': top_authors,
    }
