from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import BlogPost
from .forms import RegisterForm, BlogPostForm


from .forms import ProfileForm
from .models import Profile
# use in comment section
from django.http import HttpResponseForbidden


def home(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

    comments = Comment.objects.filter(post=post, parent=None)\
        .select_related('author')\
        .prefetch_related('replies')\
        .order_by('created_at')



def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}.')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('my_posts')
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})





@login_required
def profile(request):
    return render(request, 'blog/profile.html', {
        'profile': request.user.profile
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/edit_profile.html', {'form': form})






# Step 3: Create Views (Add, Edit, Delete)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
    return redirect('post_detail', pk=pk)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Ownership check
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Ownership check
    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment.")
    
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted!')
        return redirect('post_detail', pk=post_pk)
    
    return render(request, 'blog/delete_comment.html', {'comment': comment})