from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'profiles', api_views.ProfileRUPAPIView, basename='profile')

urlpatterns = router.urls + [
    path('post/', api_views.PostLCAPIView.as_view(), name='api_post_list'),
    path('post/<int:pk>/', api_views.PostRUPAPIView.as_view(), name='api_post_detail'),
    path('register/', api_views.RegisterAPIView.as_view(), name='api_register'),
]
