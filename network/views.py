import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Follow, User, Post


def index(request):
    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'posts': page_obj})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def create_post(request):
    print(request.POST)
    new_post = request.POST.get('post')
    print(new_post)
    if new_post:
        post = Post.objects.create(post=new_post, user=request.user)
        # post = Post(post=new_post, user=request.user)
        # post.save()
        return redirect('index')
    return redirect('index')


# @csrf_exempt
def like_post(request):
    print(request.method)
    if request.method == 'PUT':
        id = json.loads(request.body).get('id')
        post = get_object_or_404(Post, pk=id)
        if request.user in post.likers.all():
            post.likers.remove(request.user)
            count = post.likers.count()
            return JsonResponse({'message': 'You disliked this post 👎', 'color': 'secondary', 'count': count}, status=200)
        else:
            post.likers.add(request.user)
            count = post.likers.count()
            return JsonResponse({'message': 'You liked this post 👍', 'color': 'primary', 'count': count}, status=200)
    else:
        return JsonResponse({'message': 'request method are not supported'}, status=400)


def profile(request, id):
    user = get_object_or_404(User, pk=id)
    user_posts = user.creator.all()
    try:
        follow = Follow.objects.get(followed=user, follower=request.user)
        text = 'Unfollow'
        color = 'secondary'
    except ObjectDoesNotExist:
        text = 'Follow'
        color = 'danger'

    return render(request, 'network/profile.html', {'userprofile': user, 'user_posts': user_posts, 'text': text, 'color': color})


def follow(request, id):
    user1 = get_object_or_404(User, pk=id)
    if request.method == 'PUT':
        try:
            follow = Follow(followed=user1, follower=request.user)
            follow.save()
            count = user1.user_following.count()
            return JsonResponse({'message': f'you {request.user.username} followed this user {user1.username} 👍',
                                'color': 'secondary', 'count': count}, status=200)

        except IntegrityError:
            follow = Follow.objects.get(followed=user1, follower=request.user)
            follow.delete()
            count = user1.user_following.count()
            return JsonResponse({'message': f'you {request.user.username} unfollowed this user {user1.username} 👎',
                                'color': 'danger', 'count': count}, status=200)


@login_required
def following_page(request):
    users_this_user_follows = Follow.objects.filter(follower=request.user)
    posts = []
    for follow in users_this_user_follows:
        user_posts = Post.objects.filter(user=follow.followed)
        posts.append(user_posts)
    print(posts, '🌹🌹🌹')
    print(users_this_user_follows)
    return render(request, 'network/following_page.html', {'posts': posts})
