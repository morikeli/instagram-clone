from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posts, LikedPost, Comments, Friends
from .forms import CreatePostsForm
from accounts.models import UserProfile


@login_required(login_url='user_login')
def homepage_view(request):
    posted_posts = Posts.objects.all()
    upload_post = CreatePostsForm()
    get_post_id = None

    if request.method == 'POST':
        upload_post = CreatePostsForm(request.POST, request.FILES)
        get_followObj = request.POST['follow']
        get_post_id = request.POST.get('posted_id')
        get_comment_id = request.POST.get('comment')

        follow_record = Friends.objects.filter(following=request.user.userprofile, followed=get_followObj).first()
        if follow_record is None:
            new_follower = Friends.objects.create(following=request.user.userprofile, followed=get_followObj)
            new_follower.save()
            return redirect('homepage')
        else:
            unfollow = Friends.objects.get(followed=get_followObj)
            unfollow.delete()
            return redirect('homepage')
        

        if upload_post.is_valid():
            form = upload_post.save(commit=False)
            form.user = request.user.userprofile
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
    
    context = {
        'posted': posted_posts, 'UserHasLikedPost': Posts.objects.filter(id=get_post_id).exists(), 
        'create_post_form': upload_post, 'new_users': UserProfile.objects.all().exclude(name=request.user),
        'comments': Comments.objects.all(), 'followers': Friends.objects.filter().count(),

    }
    return render(request, 'users/homepage.html', context)

@login_required(login_url='user_login')
def suggested_user_profile_view(request, suggested_user):
    follow_obj = UserProfile.objects.get(id=suggested_user)
    

    context = {
        'obj': follow_obj, 'followers_posts': Posts.objects.filter(user=suggested_user),
        'posts_count': Posts.objects.filter(user=follow_obj).count(),
        'following': Friends.objects.filter(following=follow_obj).count(), 
        'followers': Friends.objects.filter(followed=follow_obj).count(),
    }
    return render(request, 'users/profile.html', context)

@login_required(login_url='user_login')
def like_posts_view(request):
    get_postId = request.GET.get('id')
    
    homepage_post = Posts.objects.get(id=get_postId)
    liked_post = LikedPost.objects.filter(id=get_postId, username=request.user.username).first()

    if liked_post is None:
        new_like = LikedPost.objects.create(username=request.user.username, id=get_postId)
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
