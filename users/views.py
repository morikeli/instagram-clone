from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.http import JsonResponse
from .models import Post, Friend, NewsFeed, Comment, Notification, SavedPost, StoryFeed, InstagramStory
from .forms import CreatePostsForm, PostInstagramStoryForm
from accounts.models import User
import random


@method_decorator(login_required(login_url='login'), name='get')
class HomepageView(View):
    form_class = CreatePostsForm
    template_name = 'core/homepage.html'


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        upload_story_form = PostInstagramStoryForm()

        # instagram stories
        user_has_story = InstagramStory.objects.filter(user_id=request.user, is_expired=False).exists() # check if request.user has any non-expired stories
        users_with_stories = InstagramStory.objects.values('user_id').distinct()    # a user can post multiple stories. To avoid 
        # duplicate values, use ".values().distinct()" to fetch unique items.

        # Retrieve profile pictures for each user
        user_profiles = {}
        for user_info in users_with_stories:
            user_id = user_info['user_id']
            story_author = User.objects.get(id=user_id)     # user who posted the story
            user_profiles[user_id] = {
                'profile_pic': story_author.profile_pic.url if story_author.profile_pic else None,
                'stories': InstagramStory.objects.filter(user_id=user_id, is_expired=False),
                'story_author': story_author.username,
            }
        
        
        # News feed
        # A News Feed contains posts that are posted by the current logged in user and/or the users he/she is following.
        # use Q to filter all posts.
        posted_items = NewsFeed.objects.filter(Q(following=request.user) | Q(post__user=request.user))
        group_ids = []
        
        for post in posted_items:
            group_ids.append(post.post_id)

        # use Q method to also filter items/media posted by the logged in user instead of items only in the 'posted_items' list.
        # this is useful especially if a user has created an account recently and isn't following any user.
        news_feed = Post.objects.filter(Q(id__in=group_ids) | Q(user=request.user)).order_by('-date_posted')
        
        # user suggestion feed
        user_following = []
        _users = User.objects.filter(is_staff=False, is_superuser=False).exclude(username=request.user)   # all users except current user, superuser or is_staff=True

        user_followers = Friend.objects.filter(follower=request.user)
        
        for followers in user_followers:
            user_list = User.objects.get(username=followers.following)
            user_following.append(user_list)
        
        suggestion_list = [person for person in list(_users) if (person not in list(user_following))]
        random.shuffle(suggestion_list[:5])     # shuffle list and get the first 5 suggested users

        # display comments
        comments_qs = Comment.objects.all()
        
        context = {
            'suggested_followers': suggestion_list,
            'posted_items': news_feed,
            'comments': comments_qs,
            'CreatePostsForm': form,
            'InstagramStoryForm': upload_story_form,
            'user_profiles': user_profiles,
            'user_has_story': user_has_story,

        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            upload_post = form.save(commit=False)
            upload_post.user = request.user
            upload_post.save()
            upload_post.save_uploaded_files(request.FILES.getlist('image'))

            messages.success(request, 'Your post was uploaded sucessfully!')
            return redirect('homepage')
        
        context = {
            'CreatePostsForm': form,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
class InstagramStoriesView(View):
    template_name = ''


    def get(self, request, *args, **kwargs):

        return JsonResponse()

@method_decorator(login_required(login_url='login'), name='get')
class SuggestedUserProfileView(View):
    template_name = 'core/profile.html'


    def get(self, request, user_id, *args, **kwargs):
        viewed_user = User.objects.get(username=user_id)
        is_following_user = Friend.objects.filter(follower=request.user, following=viewed_user).exists()
        user_following = Friend.objects.filter(follower=viewed_user).count()
        total_followers = Friend.objects.filter(following=viewed_user).count()
        total_posts = Post.objects.filter(user=viewed_user).count()
        followers_posts = Post.objects.filter(user=viewed_user)     # posts for user (following) followed/viewed by the logged in user
        _followers = Friend.objects.filter(following=viewed_user)   # followers of the 'viewed_user' object.
        _following = Friend.objects.filter(follower=viewed_user)
        saved_posts = SavedPost.objects.filter(user=viewed_user, is_saved=True)


        context = {
            'obj': viewed_user, 
            'followers_posts': followers_posts,
            'posts_count': total_posts,
            'following': user_following, 
            'followers': total_followers,
            'is_following_user': is_following_user,
            'my_followers': _followers,
            'people_i_follow': _following,
            'saved_posts': saved_posts,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
class ExplorePostsView(View):
    template_name = 'core/explore.html'

    def get(self, request, *args, **kwargs):
        posts_qs = Post.objects.all()

        context = {'posts': posts_qs}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
class SearchView(View):
    template_name = 'core/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        users_qs = User.objects.none()  # default qs if query is None.
        
        if not query is None:
            users_qs = User.objects.filter(username__contains=query).exclude(username=request.user)

        context = {'searched_users': users_qs}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
class UserNotificationsView(View):
    template_name = 'core/notifications.html'

    def get(self, request, *args, **kwargs):
        _value = request.GET.get('notification-read')
        
        if not _value is None:
            read_notification = Notification.objects.filter(receiver=request.user)
            for alert in read_notification:
                _notification = Notification.objects.get(id=alert.id)
                _notification.is_read = True    # mark notification as read
                _notification.save()

        notifications_qs = Notification.objects.filter(receiver=request.user)

        context = {'notifications': notifications_qs}
        return render(request, self.template_name, context)
