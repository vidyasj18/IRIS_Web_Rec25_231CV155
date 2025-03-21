from django.shortcuts import render
from .models import Post

# Create your views here.
# created a menu list template
def posts_list(request):
    posts = Post.objects.order_by('-date')
    return render(request, 'posts/posts_list.html',{'posts':posts})

# code for individual posts pages function to display the post
def post_page(request,slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'posts/post_page.html',{'post': post})