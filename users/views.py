from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posts, LikedPost, Comments
from .forms import CreatePostsForm


@login_required(login_url='user_login')
def homepage_view(request):
    posted_posts = Posts.objects.all()
    upload_post = CreatePostsForm()
    get_post_id = None

    if request.method == 'POST':
        upload_post = CreatePostsForm(request.POST, request.FILES)
        get_post_id = request.POST['posted_id']
        get_comment_id = request.POST['comment']

        if upload_post.is_valid():
            form = upload_post.save(commit=False)
            form.user = request.user.userprofile
            form.save()
            messages.success(request, 'Your post was uploaded successfully!')
            return redirect('homepage')
        
        else:
            post_obj = Posts.objects.get(id=get_post_id)
            new_comment = Comments.objects.create(name=post_obj, comment=get_comment_id)
            new_comment.save()
            return redirect('homepage')
    
    context = {'posted': posted_posts, 'UserHasLikedPost': Posts.objects.filter(id=get_post_id).exists(),}
    return render(request, 'users/homepage.html', context)


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


def delete_view(request):
    get_postId = request.GET['id']

    posted_img = Posts.objects.get(id=get_postId)

    if request.method == 'POST':
        get_user_response = request.POST['user_response']

        if get_user_response == 'Yes':
            get_likes_for_post = LikedPost.objects.filter(id=get_postId).all()
            posted_img.delete()
            get_likes_for_post.delete()
            messages.error(request, 'You have deleted one of your posts.')
            return redirect('homepage')
        else:
            return redirect('homepage')
    
    return redirect('homepage')