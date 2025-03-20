from django.shortcuts import render
from .models import Post

# Create your views here.
# created a menu list template
def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/posts_list.html',{'posts':posts})
