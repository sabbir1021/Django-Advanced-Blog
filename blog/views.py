from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView

class PostView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name =  'blog/post/list.html'


# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
#     return render(request,'blog/post/detail.html',{'post': post})

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/detail.html'