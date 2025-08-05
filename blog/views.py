

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Like, Post , Comment 
from accounts.models import UserProfile
import json
from django.contrib.auth.models import User
from .forms import PostForm
from django.contrib import messages
from followers.models import Follow

from django.shortcuts import get_object_or_404, redirect



@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author != request.user:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect('post_detail', slug=slug)

    if request.method == 'POST':
        username = post.author.username  # Save before deletion
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('author_profile', username=username)

    return redirect('edit_post', slug=slug)

def search_posts(request):
    query = request.GET.get('q')
    results = Post.objects.filter(title__icontains=query, published=True) if query else []
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

@login_required
def create_post(request ):
    if not request.user.is_authenticated: 
        print("⚠️ UNAUTHENTICATED submission detected!")
    if request.method == 'POST':
        
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # ✅ Assign content from Editor.js (JSON)
            content_json = request.POST.get('content')
            if content_json:
                post.content = json.loads(content_json)

            post.save()
            return redirect('author_profile' , request.user ) 
        else:
            # 🐞 Print form errors to debug
            print("❌ FORM ERRORS:", form.errors)
            print("🧪 CONTENT RECEIVED:", request.POST.get('content'))
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})




@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect('post_detail', username=post.author.username, slug=post.slug)
        
    
    

    # Handle initial content safely
    try:
        content_json = post.content if isinstance(post.content, str) else json.dumps(post.content)
        
        json.loads(content_json)  # check it's valid
    except:
        content_json = "{}"

    form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {
        "post": post,
        "form": form,
        "content_json": content_json,
    })






def post_detail(request, username, slug):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=user, slug=slug)
    authors = UserProfile.objects.select_related('user').all()[:10] 
    is_liked = False
    comments = post.comments.select_related('author').order_by('-created')  # type: ignore
    if isinstance(post.content, str):
        post_json = post.content  # already JSON string
    else:
        post_json = json.dumps(post.content)
    
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists() # type: ignore
    return render(request, 'blog/post_detail.html', {'post': post, 'post_json': post_json ,'comments': comments,  'authors': authors , 'is_liked': is_liked,})

def author_profile(request, username):
    author = get_object_or_404(User, username=username)
    profile = UserProfile.objects.get(user=author)
    is_following = False
    authors = UserProfile.objects.select_related('user').all()[:10] 
    
    
    posts = Post.objects.filter(author=author, published=True).order_by('-created')
    if request.user.is_authenticated and request.user != author:
        is_following = Follow.objects.filter(follower=request.user, following=author).exists()

    followers = Follow.objects.filter(following=author)
    following = Follow.objects.filter(follower=author)

    
    context = {
        'authors': authors ,
        'author': author,
        'profile': profile,
        'posts': posts,
        'post_count': posts.count() ,
        'is_following': is_following,
        'followers': followers,
        'following': following,
    }
    return render(request, 'blog/author_profile.html', context)



@login_required # type: ignore
def add_comment(request,username, slug):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post,author=user, slug=slug)

    if request.method == "POST":
        Comment.objects.create(
            post=post,
            author=request.user,
            body=request.POST.get("body")
        )
        return redirect('post_detail', username=username, slug=post.slug)


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()  # unlike

    return redirect('post_detail', username=post.author.username, slug=post.slug)