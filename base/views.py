from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Post, Follower, Following, Message, Friend, LikedPost
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.
def user_signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        # Create a new user
        try:
            user = User.objects.create_user(username=username, 
                password=pwd, email=email, first_name=fname, last_name=lname)
        except:
            redirect('signup')
        
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('home', pk=request.user.id)

    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home', pk=request.user.id)
        else:
            messages.add_message(request, messages.ERROR, "Incorrect Username or Password")

    if request.user.is_authenticated:
        return redirect('home', pk=request.user.id)

    context = {}
    return render(request, 'login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request, pk):
    user = UserProfile.objects.get(user_id=pk)
    post = Post.objects.filter(user_id=user.user.id)
    current_user = UserProfile.objects.get(user_id=request.user.id)
    liked_post = LikedPost.objects.filter(user_profile=current_user)

    '''
    There is an error when checking for image uploads. Specifically, when they
    don't upload a picture when tweeting. This is a crude way of dealing with the issue
    I will fix it if I come back to this. 

    Redirecting to login will just redirect them back to home if a logged in user tweets. 
    This clears the form and stops any resubmission. The point of this was to follow the
    Post/Redirect/Get (PRG) pattern. I know this is dumb and will implement a HttpResponse
    solution if I ever get back to this. 
    '''
    if request.method == 'POST' and request.POST.get('name'):
        msg = request.POST.get('tweet')
        msg = msg.lstrip()
        post_id = request.POST.get('post_id')

        if not msg:
            return redirect('login')

        if post_id:
            replying_post = Post.objects.get(id=post_id)
            try:
                pic = request.FILES['image'] #Fix
                Post.objects.create(user=current_user.user, user_profile=current_user, post=msg, 
                    image=pic, replied_to_post=replying_post)
            except:
                Post.objects.create(user=current_user.user, user_profile=current_user,post=msg, 
                    replied_to_post=replying_post)
        else:
            try:
                pic = request.FILES['image'] 
                Post.objects.create(user=user.user, user_profile=user, post=msg, 
                    image=pic)
            except:
                Post.objects.create(user=user.user, user_profile=user,post=msg)    

        return redirect('login')
    
    if request.method == 'POST' and request.POST.get('like'):
        post_id = request.POST.get('like')
        temp_post = Post.objects.get(id=post_id)
        try:
            exist = LikedPost.objects.get(Q(post=temp_post) & Q(user_profile=current_user))
        except:
            exist = None

        if exist:
            print('yes')
            delete_liked_record = LikedPost.objects.get(Q(post=temp_post) & Q(user_profile=current_user))
            delete_liked_record.delete()
            return redirect('login')
        else:
            print('no')
            new_liked = Post.objects.get(id=post_id)
            LikedPost.objects.create(post=new_liked, user_profile=current_user)
            return redirect('login')


    context = {'user':user, 'post':post, 
        'current_user':current_user, 'liked_post':liked_post}
    return render(request, 'index.html', context)


@login_required(login_url='login')
def mentions(request, pk):
    current_user = UserProfile.objects.get(user_id=pk)
    name = current_user.user.username

    post = Post.objects.filter(post__contains=name)

    context = {'post': post, 'current_user':current_user}
    return render(request, 'mentions.html', context)

@login_required(login_url='login')
def friends(request):
    user = UserProfile.objects.get(user_id=request.user.id)

    friends = Friend.objects.filter(
        Q(user1=user) | 
        Q(user2=user))

    print(type(friends))
    f_list = []
    for f in friends:
        if f.user1 == user:
            f_list.append(f.user2)
        else:
            f_list.append(f.user1)

    context = {'user':user, 'f_list':f_list}
    return render(request, 'friends.html', context)


@login_required(login_url='login')
def direct_messages(request,pk):
    user = UserProfile.objects.get(user_id=pk)
    current_user = UserProfile.objects.get(user_id=request.user.id)

    messages = Message.objects.filter(
        Q(sender_id=user.user.id, recipient_id=current_user.user.id) | 
        Q(sender_id=current_user.user.id, recipient_id=user.user.id)
            ).order_by('timestamp')

    if request.method == 'POST':
        text_content = request.POST.get('msg')

        message = Message()
        message.sender = current_user.user
        message.recipient = user.user
        message.content = text_content

        message.save()


    context = {'user':user, 'current_user':current_user, 'messages': messages}
    return render(request, 'message.html', context)


@login_required(login_url='login')
def search(request):
    current_user = UserProfile.objects.get(user_id=request.user.id)
    user_profiles = UserProfile.objects.all()
    context = {'user_profiles': user_profiles, 'current_user':current_user}

    if request.method == 'POST':
        u1 = request.POST.get('user1')
        u2 = request.POST.get('user2')

        user1 = UserProfile.objects.get(user_id=u1)
        user2 = UserProfile.objects.get(user_id=u2)

        if Friend.objects.filter(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1)).exists():
            messages.add_message(request, messages.ERROR, 
                f"Already friends with {user2.user.username}")
        else:
            Friend.objects.create(user1=user1, user2=user2)
            return redirect('friends')

    return render(request, 'search.html', context)


@login_required(login_url='login')
def profile(request, pk):
    user = UserProfile.objects.get(user_id=pk)

    if request.user.id != user.user_id:
        return redirect('login')

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')

        links = request.POST.get('link')
        location = request.POST.get('location')
        bio = request.POST.get('bio')

        if fname:
            user.user.first_name = fname
            user.user.save(update_fields=['first_name'])
        
        if lname:
            user.user.last_name = lname
            user.user.save(update_fields=['last_name'])

        if username:
            user.user.username = username
            user.user.save(update_fields=['username'])

        if links:
            user.links = links
            user.save(update_fields=['links'])

        if location:
            user.location = location
            user.save(update_fields=['location'])

        if bio:
            user.bio = bio
            user.save(update_fields=['bio'])
        
        # 
        try:
            pic = request.FILES['pic'] 
        except:
            print("Need error handing")
            pic = None
        try:
            banner = request.FILES['banner'] 
        except:
            print("Need error handing")
            banner = None

        if pic:
            user.avatar = pic
            user.save(update_fields=['avatar'])
        
        if banner:
            user.banner = banner
            user.save(update_fields=['banner'])

        print("Done")
        return redirect('login')

    context = {'user':user}
    return render(request, 'profile.html', context)

