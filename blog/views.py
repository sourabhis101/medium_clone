

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
import os
import uuid
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json, os
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from .models import Post

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Extract image URLs from post.content (which is JSON from Editor.js)
    try:
        content_json = json.loads(post.content)
        blocks = content_json.get('blocks', [])

        for block in blocks:
            if block['type'] == 'image':
                image_url = block['data']['file']['url']  # e.g. /media/uploads/img.jpg
                image_path = image_url.replace(settings.MEDIA_URL, '')  # uploads/img.jpg
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)

                if os.path.exists(full_path):
                    os.remove(full_path)

    except Exception as e:
        print("Image cleanup failed:", e)

    post.delete()
    return redirect('dashboard')  # or wherever you want to redirect





@csrf_exempt
def delete_image(request):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            image_url = data.get("url")

            if not image_url:
                return JsonResponse({"success": 0, "message": "No image URL provided"}, status=400)

            image_path = image_url.replace(settings.MEDIA_URL, "")
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)

            if os.path.exists(full_path):
                os.remove(full_path)
                return JsonResponse({"success": 1})
            else:
                return JsonResponse({"success": 0, "message": "File not found"}, status=404)

        except Exception as e:
            return JsonResponse({"success": 0, "message": str(e)}, status=500)

    return JsonResponse({"success": 0, "message": "Invalid request"}, status=400)


@csrf_exempt
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        ext = image.name.split('.')[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        filepath = os.path.join('uploads', filename)
        saved_path = default_storage.save(filepath, ContentFile(image.read()))
        file_url = default_storage.url(saved_path)

        return JsonResponse({
            "success": 1,
            "file": {
                "url": file_url
            }
        })

    return JsonResponse({"success": 0, "message": "Upload failed"}, status=400)


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def search_posts(request):
    query = request.GET.get('query')
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query)| 
            Q(content__icontains=query)).distinct()
        
        return render(request,'blog/search_results.html',{'query':query,'results':results})




def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()  # type: ignore
    liked = request.user.is_authenticated and Like.objects.filter(post=post, user=request.user).exists()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'liked': liked})

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')  # JSON from Editor.js
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect('post_detail', slug=post.slug)
    return render(request, 'blog/post_create.html')

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        text = request.POST.get('text')
        Comment.objects.create(post=post, author=request.user, text=text)
    return redirect('post_detail', slug=slug)

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', slug=slug)
