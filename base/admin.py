from django.contrib import admin
from .models import UserProfile, Follower, Following, Post, Message, Friend, LikedPost

admin.site.register(UserProfile)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(LikedPost)
