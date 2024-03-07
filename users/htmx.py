from django.contrib.auth import get_user_model
from .models import Friend, NewsFeed, Post, Comment, Notification, SavedPost
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import PostInstagramStoryForm


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


def follow_or_unfollow_viewed_user(request, user_id):
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


def follow_or_unfollow_users_in_profile_page(request):
    """ This function allows a logged in user to follow/unfollow other users via modal forms in his/her profile page. """

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
    
    return redirect('user_profile')


def like_or_unlike_post(request):
    """ This function allows a user to like or unlike a post. """

    _reaction = request.POST.get('like-unlike')

    if not _reaction is None:
        post_obj = Post.objects.get(id=_reaction)
        is_available = Post.objects.filter(total_likes=request.user, id=_reaction).exists()    # check if the user has liked the post
        notification_exists = Notification.objects.filter(post=post_obj).exists()

        if is_available:    # True
            get_post_qs = Post.objects.get(id=_reaction)
            get_post_qs.total_likes.remove(request.user)
            get_post_qs.liked_by_user = None
            get_post_qs.is_liked = False
            get_post_qs.save()

            if notification_exists and not (request.user == post_obj.user):     # if notification exists - True
                _notify = Notification.objects.get(
                    post=post_obj,
                    sender=request.user,
                )
                _notify.delete()
        
        else:
            get_post_qs = Post.objects.get(id=_reaction)
            get_post_qs.total_likes.add(request.user)
            get_post_qs.liked_by_user = request.user
            get_post_qs.is_liked = True
            get_post_qs.save()

            # send notification
            if not (request.user == post_obj.user):   # only send notification when the user is not the owner of the post
                _notify = Notification.objects.get_or_create(
                    post=post_obj,
                    sender=request.user,
                    receiver=post_obj.user,
                    notification_type=1,

                )
                _notify
    
    return redirect('homepage')


def like_or_unlike_comment(request):
    """ This function allows a user to like or unlike a comment on a given post. """

    _reaction = request.POST.get('like-unlike-comment')
    get_post_id = request.POST.get('commented-post')


    if not _reaction is None:
        post_obj = Post.objects.get(id=get_post_id)
        comment_obj = Comment.objects.get(id=_reaction)
        is_available = Comment.objects.filter(total_likes=request.user, id=_reaction).exists()    # check if the user has liked the comment
        notification_exists = Notification.objects.filter(post=post_obj).exists()

        if is_available:    # True
            get_comment_qs = Comment.objects.get(id=_reaction)
            get_comment_qs.total_likes.remove(request.user)
            get_comment_qs.liked_by_user = None
            get_comment_qs.is_liked = False
            get_comment_qs.save()

            if notification_exists:     # if notification exists - True
                _notify = Notification.objects.get(
                    post=post_obj,
                    sender=request.user,
                    receiver=comment_obj.author,
                    notification_text=comment_obj.comment[:30],
                    notification_type=4,
                )
                _notify.delete()
        
        else:
            get_comment_qs = Comment.objects.get(id=_reaction)
            get_comment_qs.total_likes.add(request.user)
            get_comment_qs.liked_by_user = request.user
            get_comment_qs.is_liked = True
            get_comment_qs.save()

            # send notification
            _notify = Notification.objects.get_or_create(
                post=post_obj,
                comment=comment_obj,
                sender=request.user,
                receiver=comment_obj.author,
                notification_text=comment_obj.comment[:30],
                notification_type=4,
            )
            _notify

    return redirect('homepage')


def add_comment(request):
    user_comment = request.POST.get('comment')
    _post = request.POST.get('post')

    if user_comment:
        post_obj = Post.objects.get(id=_post)
        create_comment = Comment.objects.get_or_create(author=request.user, item=post_obj, comment=user_comment)

        # send notification
        get_saved_comment = Comment.objects.get(item=post_obj, comment=user_comment)

        if not (request.user == post_obj.user):
            _notify = Notification.objects.get_or_create(
                post=post_obj,
                sender=get_saved_comment.author,
                receiver=get_saved_comment.item.user,
                notification_text=get_saved_comment.comment[:30],
                notification_type=2,
            )
        
        messages.success(request, 'Comment submitted successfully!')
        return redirect('homepage')

    return redirect('homepage')
   

def delete_post(request):
    delete_request = request.POST.get('delete-post')

    if not delete_request is None:
        get_post = Post.objects.get(id=delete_request)
        get_post.delete()

        messages.error(request, 'Post deleted successfully!')
        return redirect('homepage')


    return redirect('homepage')


def delete_comment(request):
    delete_request = request.POST.get('delete-comment')

    if not delete_request is None:
        get_comment = Comment.objects.get(id=delete_request)
        get_comment.delete()

        messages.error(request, 'Comment deleted successfully!')
        return redirect('homepage')


    return redirect('homepage')


def save_favorite_posts(request):
    save_request = request.POST.get('add-to-favorites')
    
    if not save_request is None:
        post_obj = Post.objects.get(id=save_request)
        saved_post_exists = SavedPost.objects.filter(user=request.user, favorite_post=post_obj).exists()
        
        if saved_post_exists:   # True
            get_favorite_post = SavedPost.objects.get(user=request.user, favorite_post=post_obj)
            get_favorite_post.delete()
        
        else:
            _, created = SavedPost.objects.get_or_create(user=request.user, favorite_post=post_obj, is_saved=True)


    return redirect('homepage')


def upload_instagram_story(request):
    """ This function allows a user to update his/her instagram stories. """

    form = PostInstagramStoryForm()

    if request.method == 'POST':
        form = PostInstagramStoryForm(request.POST, request.FILES)

        if form.is_valid():
            create_story = form.save(commit=False)
            create_story.user = request.user
            create_story.save()

            messages.success(request, 'Instagram story posted successfully!')
            return redirect('homepage')

    return redirect('homepage')