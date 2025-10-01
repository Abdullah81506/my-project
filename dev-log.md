1. Building Posts Model
    in models.py:
    if we are storing images we need to set the path for them and for that in settings under static url, 
    *** MEDIA_ROOT = BASE_DIR/ 'upload'
    this 'upload' will be a folder wherein another folder will be present and images will be stored there.

2. Structuring Templates
    we'll have a template folder at the root of the project and django needs to be aware of that folder we'll add on our own. so in settings under templates, 
    ***  'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
    SETTINGS_PATH is the name of the variable which is defined in settings.py 
    *** SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
    now we can create the template folder.

3. Configuring Static files and Render Post
    to configure static files, just simply use the key in context from views and call the fields where u want them to in the html files. like
    ***   {{post.content}} # post is the key from the context and content is the field or column
    we can also use filters for our fields for instance for the datetime field if we just wanna show the date instead of updating our model and going through all the migration process just use filter like 
    {{post.last_updated | date}}

4. Building Tags
    Tags are related to posts. they share a many-many relationship. each post can have many tags and each tag can show us many posts. build a tags model and define a method in it that will automatically generate its slug.

5. Recording Views
    define an integer field in post model to record views. we'll also define a logic in views.py that when a particular post page is requested view will check the count value for the post and if its null, it will set to 1 and increment it everytime that post is requested and save it in db. use pluralize filter to add suffix if the value is more than one like 
    *** You have {{post.view_count}} message{{post.view_count|pluralize:'es'}} 

6. Allow users to comment
    each comment will be linked to a post. establish the connection using a foreign key. and each comment is from an author link it to the User which is from django. link it using foreign key. using models.CASCADE means that if the referenced object (object of parent class) is deleted, delete this object (from child class) too.. 
    form for a comment is also needed so make forms.py and make a form. now pass it to the template. 

7. Fixing the submit issue on refresh
    whenever the comment is posted, the post request is being submitted everytime on refresh. meaning that the same comment may be rendered more than once. to fix this, import reverse and httpresponseredirect from django and redirect the user to the post page url which invalidates the post request.

8. Displaying popular and new posts on home
    make an instance of top and recent posts in views.py by sorting them in an order of most views and most recently posted. then access them in template where required.

9. Making users subscribe to the blog:
    create a subscribe model and a subscribe form. make an instance of subscribe form in views.py and check if the form is valid to save the user as a subscriber. also make an instance of success message if subscribe is successful. access that form in the template where required and using if condition, display the success message.

10. Adding featured post
    update the post model and add a boolean field for a featured post. boolean because featured post will either exist or not (true or false). make an instance of the featured post by setting the field to true. if there are more than 1 featured blogs, show only the first featured one. and in the template using if statement diaplay it with some filters like "truncatechars" to shorten the content.

11. Building tags page
    make a view and a url for tags page. make an instance of Tag model in view and access it in template.

12. Enabling author on posts
    for this we will link post model to an inbuilt user model. meaning that we wont have to create one. create a foreign key in post model with the parent being user. however that inbuilt model doesnt contain the fields like image or slug. which ofcourse will be needed for authors profile and its own page. for that create a new model and establish 1-1 between the inbuilt user and this.

13. Building authors page
    make a view and a url for author page just like tags page. make an instance of Profile model in view and access it in template. to show top authors import 'count' and 'user' in views from django and make an instance of
    top authors by getting them, counting their number of posts and sorting them in descending order. this is done using annotate() which creates a count of something(post) for every object in the model(author).
    *** annotate(): add a count              *** order_by: sort using that count

14. Building Search
    create a search url and view and its template. in view make an empty variable for search and check if the get request has the parameter "q" which is search text entered by user in search box and if query exists store it in variable and then get all posts in a var and match its title with that query searched by user and pass posts and search query in template using context. in form, use an input with name='q' so django knows where to look loop through posts and show matching results.
    *** request.GET.get('q') means:
        "Get the value of q from the URL like /search/?q=python"

15. Building website meta
    this is the part of website that talks about the website like about, home and the website title. hardcoding this is not a good practice because if u want to make some changes, u will eventually need a developer who will do the job and deploy again. instead, storing such information in the database is more efficient so whenever changes are needed it will be made using the admin panel. for that a model is required.

16. Allowing Html content
    When we enter content through the Django admin panel, any HTML tags like <b>, <i>, or <p> are shown as plain text and not rendered. To allow formatting we can use a tool like tiny.cloud to generate styled HTML content and paste that into the content field in the admin panel. However, if we simply display the content using
    {{ post.content }}, the HTML tags will appear as text. To fix this, we use the safe filter like
    {{ post.content|safe }} Its important not to wrap this in a any tag, because the HTML content might already include block-level tags like <div> or <p>, which could break the layout or cause scroll issues.

17. Sessions
    It is a way using which a server keeps track of the behaviour by storing some data on the client which is then used by the server to identify the client. django maintains a unique identifier 'session id' to keep track of every client. this identifier is stored as a cookie on the browser and is sent to the server with request.
    after user has subscribed, using sessions hide the subscription form and redirect to the same page. 

18. Enabling Authentication and Inbuit Views
    Django has an inbuilt Authentication which provides us with many tools like a User model, inbuilt views, urls, functions like login, logout and we just need to enable them. First enable path in root urls with 
    *** path('accounts/', include('django.contrib.auth.urls')), this is activate many other urls like login logout etc. 

19. Implementing Login funtionality
    create a folder in templates for registeration and create a login template in there. when we enabled accounts path in root url it gave us access to a lot of tools like urls and in built forms. render that form in template and direct it to the page you wish. because by default it will direct to profiles url which is also built-in, to do that in settings.py paste this 
    *** LOGIN_REDIRECT_URL = '/'        "/" means homepage  
    we can also render a basic html form to include placeholders because inbuilt form doesnt provide that but the names of that form must match the names of inbuilt form

20. Implementing Logout Functionality
    create a logout template. the name of the templated MUST be 'logged_out' because the inbuilt logout url will look for a template by this name. when the user will have logged out, django will show the admin-like url page not the template which we have created because in settings.py under installed apps, admin is given priority over auth. we can simply place the admin app line under auth and out django will prioritize our template.

21. Conditional Rendering
    its best to implement this to show login/signup button for logged out users and logout button for logged in users. best to do this is in base template. using inbuilt boolean property '.is_authenticated', show logout button, else login/signup buttons. however, if the fields do not match, like if password is wrong, display error using '.non_field_errors'. Do this in login page.

22. Building Registration form
    Django gives us some built-in URLs, views, and models for authentication like login and logout. But if we want a signup feature, we have to make it ourselves. We create a path, a view, and a template for the signup page.  Django has a built-in form called UserCreationForm, which we can use to create a user. We import this in forms.py and make our own custom form by inheriting from it. This built-in form uses Django's inbuilt User model. In the form, we can add our own validation rules. Even though Django does some validation by default, it doesn't check for things like unique email or allow us to easily add placeholders — that's why we do it manually. In the view, we display the form and log the user in using Django’s login() function. This function is only needed when we're handling the signup/login ourselves. If we use the built-in accounts/ path, Django handles login/logout on its own.

23. Building Bookmarks
    bookmarks can only be made by authenticated users who have registered on the app. update post model and add many-many field. the relationship is to be established with inbuilt user model. create url then create a view for bookmark and get the post user is interacting with in a variable using function 'get_object_or_404'. we can do this with Post.objects.get() but if the post doesnt exist, this will crash the site whereas the function will carefully handle the error. in template if post is bookmarked, show remove bookmark button and vice versa.
    also handle unauthenticated interctions if user has logged in only then bookmark should be allowed otherwise should be directed to the login page.

24. Building Likes
    the same logic for bookmarks applies for likes. infact, its common pattern in django for (fav, votes, bookmarks, likes). however there is one addition to display count of likes. for that in models define a method to return count of the likes field, in post page view get that method in an instance and render it in template.

25. Building all bookmarks, posts, and likes page
    make a path and a template for the page. make a view and get all bookmarked posts using bookmark field. render it in the template and show the bookmarks link to authorized users only. same logic applies for all posts and all likes. get all posts and all likes in a variable inside separate views. 

**** we can use js code for redirect to the previous page like "javascript:history.back()"

26. Building Password reset feature
    since we have already defined path in urls.py of root, we dont need to define d=separate paths for poassword rest. just make templates and render the built-in form or a custom form if you wish. inherit from base file. make sure the files have specific names because since django will do all the work, it will look for templates with a specific name. in settings, do this :


    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'abdullahjavaid81506@gmail.com'       # Replace with your Gmail
    EMAIL_HOST_PASSWORD = 'inazmtorhnpazcdb'     # NOT your normal password!

    this will set the app in such a way that when user gives their email for password reset they will recieve message at the given account if its stored in the database

27. Context-Processor
    this is a way to make certian variables available to all templates without having to pass them manually everytime in views. like in footer there is a subscription form which has to be in every page, so we simply mak a file in apps and pass that variable. this is a manually created file, so django needs to be aware of it. configure the settings in templates and add the file name. 

28. Creating subscribe feature
    create a subscribe model 1-1 related with the inbuilt user model and add email field. also create the subscribe view to handle the logic once the subcription button is pressed. create a url for that as well since a new view is being created. also. this subscribe form is in footer which exists on every page. so create an instance of the form in context-processor to avoid dry coding. 

29. Creating unsubscribe feature
    create a url, a view and a form in template whose action map to the unsubscribe url. in view delete the user from the subscribe model using .delete() and redirect to the page user was on. also add a confirmation step to prevent accidental unsubscriptions using js "onsubmit" in form.
    
30. Creating profile dropdown
    in base template if user is logged in simply show its profile picture and a link to all their posts. and a logout in the dropdown that logs the user out. 

31. Creating authors all_posts page
    the authors page made previously only had top and recent posts. this new page will contain all posts by author and it will be linked to the profile image of user in base template which was just added.

32. Implementing create on frontend for posts
    implementing crud on frontend enables all users to manage their posts putside of admin panel. for that create a form in forms.py using the post model and add the necessary fields in it. create a view and get the author make an instance of the new form set the author of the post to the currectly logged in user create slug and save it. then save many-many data that is tags in this case, because for saving many-many data, it is important for the record to exist in the table because this relationship creates a separate table to relate records of existing table. then create a template and render the form.
    
33. Implementing edit on frontend for posts    
    for edit create a view that takes post id of the post to be edited. do the same as create but bind the form to an existing post, using instance so it knows its being edited not created. and as for the template, no need to create new, work with the create post template but url is still needed. but in template render conditions for create and edit such as for headings or page title

34. Implementing delete on frontend for posts
    create a url and a view. in view get the post of the author and simply delete the post using .delete() in template using post.author that is the author of the post, render condition that shows the edit and the delete option to only the author of that post. also handle condition for other than author himself and display some forbidden response if anyone tries to access that url manually or through get request. 

35. Allowing users to delete comments
    to allow users to delete their own comments, they will have to identified as the owner of that comment. using author field in comment that is related to the built-in model user, identify the user. make a view get the comment through its id also get the slug of the post currently on to redirect once the comment is deleted and delete the comment. also make a url for it as well. at last render the url of that delete in a form with a button and verify if the user is the owner of that comment

36. Implementing edit for users
    make a url and a form since the app has used the built-in user model and linked it to a custom model for the user of the app, to edit their fields, 2 separate forms are needed. make two models render them in view check if those forms are valid and save them. make a template and render both forms. 

37. Using APIs 
    this tool is an alternate of rendering html pages. mainly to enjoy frontend independence. for that install djangorestframework and make a separate file (optional) for api_views. make a file for serializers which helps convert complex data types in easier formats like json that can be sent over an api. they also help do the reverse when displaying data on UI. import post model and make a serializers and get all fields. the same way as in forms.py in api views import those serializers and using "queryset" get all objects of the desired model. this queryset tells view which data needs to be worked upon. and using "serializers_class" make an instance of the serializer just created. this will tell view how to turn data in json which serializers in .py will do that. and in api_urls fetch those views from api_view and link them to urls.

38. Implementing JWT Authentication
    building a secure api with drf and jwt authentication. in settings.py configure drf to use jwt authentication
    meaning making django aware to use jwt tokens for all api views. In root urls, setup routes for jwt authentication in django api. this is done in root urls just like for django authentication 'accounts/'. make a custom permission class to allow safe and unsafe methods to certain users. put it in a separate file for scalability. and pass this permission class in api views for retrieve update and delete api view. no need for create view because the one creating is the author so no need to check that. only authors should be able to handle update and delete for their posts.
    
    