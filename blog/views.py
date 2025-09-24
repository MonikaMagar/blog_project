from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Post
from .forms import PostForm
import requests
from django.contrib import messages


# -------------------------
# Home Page
# -------------------------
def home(request):
    return render(request, "blog/home.html")


# -------------------------
# List All Posts
# -------------------------
def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})


# -------------------------
# Create a New Post
# -------------------------
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "action": "Create"})


# -------------------------
# Update a Post
# -------------------------
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "action": "Update"})


# -------------------------
# Delete a Post
# -------------------------
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        post_title = post.title
        post.delete()
        messages.success(request, f'Post "{post_title}" was deleted successfully!')
        return redirect("post_list")
    
    return redirect("post_list")  # skip confirmation page



# -------------------------
# Fetch External Posts from MockDog API
# -------------------------
def fetch_external_posts(request):
    url = "https://mockdog.dev/api/dogs?count=10"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()  # List of dog objects
        for item in data:
            Post.objects.get_or_create(
                title=item.get("name", "Unknown Dog"),
                defaults={
                    "content": item.get("breed", "Unknown breed"),
                    "author": "MockDog API",
                    "image": item.get("image", "")
                }
            )
    return redirect("post_list")


# -------------------------
# Chart Page
# -------------------------
def chart(request):
    posts = Post.objects.all()
    counts = posts.values("author").annotate(count=Count("id"))
    labels = [c["author"] for c in counts]
    data = [c["count"] for c in counts]
    return render(request, "blog/chart.html", {"authors": labels, "counts": data})
