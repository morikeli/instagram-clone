from django.contrib.auth import get_user_model
from .models import Friend, LikedPost, NewsFeed, Post
from django.shortcuts import redirect


def follow_or_unfollow_users_homepage(request):
    """ This function allows a user to follow or unfollow suggested users. """

    _user = request.POST.get('follow-user')
    user_instance = get_user_model().objects.get(username=_user)    # create user instance

    if not _user is None:
        user_is_following = Friend.objects.filter(follower=request.user, following=user_instance)

        if user_is_following:
            unfollow_user = Friend.objects.get(follower=request.user, following=user_instance)
            unfollow_user.delete()  # delete user who is followed by the logged in user

            delete_posts = NewsFeed.objects.filter(user=request.user, following=user_instance)
            delete_posts.delete()   # delete post of the user followed by the logged in user
        
        else:
            follow_user = Friend.objects.get_or_create(follower=request.user, following=user_instance)
    
    return redirect('homepage')


def follow_or_unfollow_users_in_profile_page(request, user_id):
    """ This function allows a user to follow or unfollow other users in their profile page. """

    _user = request.POST.get('follow-user')
    user_instance = get_user_model().objects.get(username=_user)    # create user instance

    if not _user is None:
        user_is_following = Friend.objects.filter(follower=request.user, following=user_instance).exists()

        if user_is_following:
            unfollow_user = Friend.objects.get(follower=request.user, following=user_instance)
            unfollow_user.delete()

            delete_posts = NewsFeed.objects.filter(user=request.user, following=user_instance)
            delete_posts.delete()   # delete post of the user followed by the logged in user
        
        else:
            follow_user = Friend.objects.get_or_create(follower=request.user, following=user_instance)
    
    return redirect('view_user_profile', user_id)


def like_or_unlike_post(request):
    """ This function allows a user to like or unlike a post. """

    _reaction = request.POST.get('like-unlike')

    if not _reaction is None:
        is_available = LikedPost.objects.filter(user=request.user, post=_reaction).exists()    # check if the user has liked the post
        
        if is_available:    # True
            get_post_qs = Post.objects.get(id=_reaction)
            get_post_qs.total_likes -= 1
            get_post_qs.save()

            delete_like = LikedPost.objects.get(user=request.user, post_id=_reaction)
            delete_like.delete()    # delete like record from db.
        
        else:
            get_post_qs = Post.objects.get(id=_reaction)
            get_post_qs.total_likes += 1
            get_post_qs.save()

            user_has_liked = LikedPost.objects.get_or_create(user=request.user, post_id=_reaction)
    
    return redirect('homepage')


