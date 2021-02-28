from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Comment
from django.views.generic import ListView,DetailView
from .forms import EmailPostForm , CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator
from django.db.models import Count

# class PostView(ListView):
#     model = Post
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name =  'blog/post/list.html'
    
def post_list(request,tag_slug=None):
    posts = Post.published.all()
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'blog/post/list.html',{'posts': page_obj,'page_obj':page_obj,'tag':tag})



def post_detail(request,pk, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,
    'blog/post/detail.html',
    {'post': post,
    'comments': comments,
    'new_comment': new_comment,
    'comment_form': comment_form,
    'similar_posts': similar_posts})
    
    return render(request,'blog/post/detail.html',{'post': post})

# class PostDetailView(DetailView):
#     model = Post
#     context_object_name = 'post'
#     template_name = 'blog/post/detail.html'

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'chasibaribd@gmail.com',
            [cd['to']])
            sent = True
            
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
        'form': form,'sent': sent})
