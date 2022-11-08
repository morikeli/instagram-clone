from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Posts, LikedPost

@login_required(login_url='user_login')
def homepage_view(request):
    posted_posts = Posts.objects.all()
    
    context = {'posted': posted_posts}
    return render(request, 'users/homepage.html', context)


def like_posts_view(request):
    get_postId = request.GET.get('id')
    print(f'Post id: {get_postId}')
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
