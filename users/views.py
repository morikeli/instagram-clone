from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Posts, LikedPost, Comments, Friends
from .forms import CreatePostsForm
from accounts.models import User
from itertools import chain
import random

@login_required(login_url='user_login')
def homepage_view(request):
    posted_posts = Posts.objects.all()
    upload_post = CreatePostsForm()
    get_post_id = None

    if request.method == 'POST':
        upload_post = CreatePostsForm(request.POST, request.FILES)
        get_followObj = request.POST.get('follow')
        get_post_id = request.POST.get('posted_id')
        get_comment_id = request.POST.get('comment')

        if get_followObj is not None:
            follow_record = Friends.objects.filter(following=request.user, followed=get_followObj).first()

            if follow_record is None:
                new_follower = Friends.objects.create(following=request.user, followed=get_followObj)
                new_follower.save()
                return redirect('homepage')
            else:
                unfollow = Friends.objects.get(followed=get_followObj, following=request.user)
                unfollow.delete()
                return redirect('homepage')
            
        else:

            if upload_post.is_valid():
                form = upload_post.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, 'Your post was uploaded successfully!')
                return redirect('homepage')
            else:
                try:
                    post_obj = Posts.objects.get(id=get_post_id)
                    new_comment = Comments.objects.create(id=get_post_id, name=post_obj, comment=get_comment_id)
                    new_comment.save()
                    return redirect('homepage')
                except Posts.DoesNotExist:
                    return redirect('homepage')
    
    # Posts feed - Current user should see posts for followers he/she is following
    my_followers = []
    my_feed = []

    user_followers = Friends.objects.filter(following=request.user)
    
    for f in user_followers:
        my_followers.append(f.followed)     # append users I'm following in this list
    
    for users in my_followers:
        feed_list = Posts.objects.filter(user__username=users)    # get posts of people I'm following
        my_feed.append(feed_list)   # append the posts in this list

    post_feed = list(chain(*my_feed))
    
    # user suggestion feed
    all_users = User.objects.filter(is_staff=False, is_superuser=False).all().exclude(username=request.user)   # exclude superuser and staff users
    user_following = []

    for followers in user_followers:
        user_list = User.objects.get(username=followers.followed)
        user_following.append(user_list)

    new_suggestion_list = [person for person in list(all_users) if (person not in list(user_following))]
    final_suggestion_list = [person for person in list(new_suggestion_list) if (person not in list(User.objects.filter(username=request.user.username)))]
    random.shuffle(final_suggestion_list)
    
    context = {
        'posted': post_feed, 'UserHasLikedPost': LikedPost.objects.filter(user=request.user), 
        'create_post_form': upload_post, 'new_users': final_suggestion_list[:3],
        'comments': Comments.objects.all(), 'followers': Friends.objects.filter().count(),
        'my_friends': Friends.objects.filter(following=request.user).all()

    }
    return render(request, 'users/homepage.html', context)

@login_required(login_url='user_login')
def suggested_user_profile_view(request, suggested_user):
    viewed_user = User.objects.get(id=suggested_user)

    if request.method == 'POST':
        get_followObj = request.POST.get('follow')

        if get_followObj is not None:
            follow_record = Friends.objects.filter(following=request.user, followed=get_followObj).first()
            
            if follow_record is None:
                new_follower = Friends.objects.create(following=request.user, followed=get_followObj)
                new_follower.save()
                return redirect('follow_user_profile', suggested_user)
            
            else:
                unfollow = Friends.objects.get(followed=get_followObj)
                unfollow.delete()
                return redirect('follow_user_profile', suggested_user)
    
    context = {
        'obj': viewed_user, 'followers_posts': Posts.objects.filter(user=suggested_user),
        'posts_count': Posts.objects.filter(user=viewed_user).count(),
        'following': Friends.objects.filter(following=viewed_user).count(), 
        'followers': Friends.objects.filter(followed=viewed_user).count(),
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='user_login')
def like_posts_view(request):
    get_postId = request.GET.get('id')
    
    homepage_post = Posts.objects.get(id=get_postId)
    liked_post = LikedPost.objects.filter(post_id=get_postId, user=request.user.username).first()

    if liked_post is None:
        new_like = LikedPost.objects.create(user=request.user.username, post_id=get_postId)
        homepage_post.total_likes += 1
        new_like.save()
        homepage_post.save()
        return redirect('homepage')
    
    else:
        liked_post.delete()
        homepage_post.total_likes -= 1
        homepage_post.save()
        return redirect('homepage')

@login_required(login_url='user_login')
def delete_posts_view(request):
    get_postObj = request.GET.get('id')
    posted_img = Posts.objects.get(id=get_postObj)

    if posted_img is not None:
        get_likes_for_post = LikedPost.objects.filter(id=get_postObj).all()
        posted_img.delete()
        get_likes_for_post.delete()
        messages.error(request, 'You have deleted one of your posts.')
        return redirect('homepage')
    else:
        return redirect('homepage')
