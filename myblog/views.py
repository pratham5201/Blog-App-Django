# myblog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm, CategoryForm, TagForm
from django.contrib.auth.decorators import login_required, user_passes_test
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def can_delete_post(user, post):
    return user == post.author

def can_delete_comment(user, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    return user == comment.author

@login_required(login_url='login')  # Redirect to the login page if not logged in
def root_view(request):
    posts = Post.objects.all()
    return render(request, 'myblog/post_list.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'myblog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'myblog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Trigger WebSocket update
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "post_group", {"type": "post_update", "message": "New post created"}
            )

            messages.success(request, 'Post created successfully.')
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'myblog/post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            form.save_m2m()  # Save many-to-many fields
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'myblog/post_form.html', {'form': form, 'action': 'Update'})

@user_passes_test(can_delete_post)
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'myblog/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'myblog/category_form.html', {'form': form, 'action': 'Create'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'myblog/category_form.html', {'form': form, 'action': 'Update'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

# Tag views
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'myblog/tag_list.html', {'tags': tags})

@login_required
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'myblog/tag_form.html', {'form': form, 'action': 'Create'})

@login_required
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'myblog/tag_form.html', {'form': form, 'action': 'Update'})

@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect('tag_list')

# Comment views
@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # Trigger WebSocket update
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"post_{post_pk}_group", {"type": "comment_update", "message": "New comment created"}
            )

            messages.success(request, 'Comment created successfully.')
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm()

    return render(request, 'myblog/comment_form.html', {'form': form})

# @user_passes_test(can_delete_comment)
# @user_passes_test(lambda u: can_delete_comment(u, pk), login_url='/login/')
@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def can_delete_post(user, post):
    return user == post.author

def can_delete_comment(user, comment):
    return user == comment.author
