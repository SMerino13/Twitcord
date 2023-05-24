from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='static/img/discord-icon.svg')
    bio = models.TextField(max_length=200, null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True, default='static/img/header.jpg')
    links = models.CharField(max_length=50, null=True, blank=True)
    num_of_following = models.IntegerField(null=False, blank=True, default=0)
    num_of_followers = models.IntegerField(null=False, blank=True, default=0)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    '''
    The number of replies, retweets, and likes are currently not being counted
    on the front end. 
    '''
    replies = models.IntegerField(null=True, blank=True)
    retweets = models.IntegerField(null=True, blank=True)
    likes = models.IntegerField(null=True, blank=True)
    
    replied_to_post = models.ForeignKey('self', null=True, blank=True, related_name= 'parent_post', on_delete=models.CASCADE)
    post = models.TextField(null=False)
    image = models.ImageField(null=True, blank=True, upload_to='post_images/')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'{self.id}: {self.post[:30]}'
    
class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Post: {self.post.post[:30]}'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    img = models.ImageField(upload_to='message/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username}, To: {self.recipient.username}, Content: {self.content}"

    class Meta:
        ordering = ['-timestamp']

class Friend(models.Model):
    user1 = models.ForeignKey(UserProfile, related_name='user1_friends', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name='user2_friends', on_delete=models.CASCADE)
    established = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user1', 'user2'], ['user2', 'user1']]

    def __str__(self):
        return f'{self.user1.user.username} - {self.user2.user.username}'