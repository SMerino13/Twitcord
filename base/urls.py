from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('home/<str:pk>/', views.home, name='home'),
    path('mentions/<str:pk>/', views.mentions, name='mentions'),
    path('friends/', views.friends, name='friends'),
    path('search/', views.search, name='search'),
    path('message/<str:pk>/', views.direct_messages, name='dm'),
    path('profile/<str:pk>/', views.profile, name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)