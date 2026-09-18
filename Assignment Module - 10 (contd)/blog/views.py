from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Q, Prefetch
from django.http import JsonResponse, HttpResponseForbidden

from .models import BlogPost, Comment, PostLike, CommentLike, PostRating, Profile, Category
from .forms import (
    RegisterForm, BlogPostForm, CommentForm, ReplyForm,
    RatingForm, ProfileForm, SearchForm
)


# ==================== AUTH ====================

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


# ==================== POSTS ====================

# def home(request):
#     posts = BlogPost.objects.select_related('author').annotate(
#         like_count=Count('likes', distinct=True),
#         comment_count=Count('comments', distinct=True),
#         avg_rating=Avg('ratings__rating'),
#         rating_count=Count('ratings', distinct=True),
#     ).order_by('-created_at')
#     return render(request, 'blog/home.html', {'posts': posts})




def home(request):
    categories = Category.objects.prefetch_related(
        Prefetch(
            'posts',
            queryset=BlogPost.objects.select_related('author', 'category').annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True),
                avg_rating=Avg('ratings__rating'),
                rating_count=Count('ratings', distinct=True),
            ).order_by('-created_at')
        )
    ).annotate(post_count=Count('posts')).filter(post_count__gt=0)

    # Posts that have no category
    uncategorized = BlogPost.objects.filter(category__isnull=True).select_related('author').annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
        avg_rating=Avg('ratings__rating'),
        rating_count=Count('ratings', distinct=True),
    ).order_by('-created_at')

    return render(request, 'blog/home.html', {
        'categories': categories,
        'uncategorized': uncategorized,
    })




def post_detail(request, pk):
    post = get_object_or_404(
        BlogPost.objects.select_related('author').annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True),
            avg_rating=Avg('ratings__rating'),
            rating_count=Count('ratings', distinct=True),
        ),
        pk=pk
    )

    # Prefetch top-level comments + their replies + likes
    comments = Comment.objects.filter(post=post, parent=None).select_related(
        'author'
    ).prefetch_related(
        Prefetch('replies', queryset=Comment.objects.select_related('author').order_by('created_at')),
        'likes'
    ).annotate(like_count=Count('likes')).order_by('created_at')

    user_liked = False
    user_rating = None
    if request.user.is_authenticated:
        user_liked = PostLike.objects.filter(post=post, user=request.user).exists()
        user_rating = PostRating.objects.filter(post=post, user=request.user).first()

    comment_form = CommentForm()
    rating_form = RatingForm(instance=user_rating) if user_rating else RatingForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_liked': user_liked,
        'user_rating': user_rating,
    }
    return render(request, 'blog/post_detail.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
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
        form = BlogPostForm(request.POST, request.FILES, instance=post)
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
    posts = BlogPost.objects.filter(author=request.user).annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
        avg_rating=Avg('ratings__rating'),
    )
    return render(request, 'blog/my_posts.html', {'posts': posts})


# ==================== COMMENTS ====================

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
def add_reply(request, comment_id):
    parent = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent.post
            reply.author = request.user
            reply.parent = parent
            reply.save()
            messages.success(request, 'Reply added!')
    return redirect('post_detail', pk=parent.post.pk)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden('You cannot edit this comment.')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author != request.user:
        return HttpResponseForbidden('You cannot delete this comment.')
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted!')
        return redirect('post_detail', pk=post_pk)
    return render(request, 'blog/delete_comment.html', {'comment': comment})


# ==================== LIKES ====================

@login_required
def toggle_post_like(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        messages.info(request, 'Post unliked.')
    else:
        messages.success(request, 'Post liked!')
    return redirect('post_detail', pk=pk)


@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect('post_detail', pk=comment.post.pk)


# ==================== RATINGS ====================

@login_required
def rate_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        existing = PostRating.objects.filter(post=post, user=request.user).first()
        form = RatingForm(request.POST, instance=existing)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.post = post
            rating.user = request.user
            rating.save()
            messages.success(request, 'Rating saved!')
    return redirect('post_detail', pk=pk)


# ==================== SEARCH ====================

def search(request):
    form = SearchForm(request.GET or None)
    posts = BlogPost.objects.none()
    query = ''
    if form.is_valid():
        query = form.cleaned_data.get('q', '').strip()
        if query:
            posts = BlogPost.objects.select_related('author', 'category').filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)|
                Q(category__name__icontains=query)
            ).annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True),
                avg_rating=Avg('ratings__rating'),
            ).distinct()
    return render(request, 'blog/search_results.html', {
        'form': form,
        'posts': posts,
        'query': query,
    })


# ==================== POPULAR POSTS ====================

def popular_posts(request):
    posts = BlogPost.objects.select_related('author').annotate(
        like_count=Count('likes', distinct=True),
        comment_count=Count('comments', distinct=True),
        avg_rating=Avg('ratings__rating'),
        rating_count=Count('ratings', distinct=True),
        engagement=Count('likes', distinct=True) + Count('comments', distinct=True),
    ).order_by('-engagement', '-avg_rating', '-like_count')[:20]
    return render(request, 'blog/popular_posts.html', {'posts': posts})


# ==================== PROFILE ====================

@login_required
def profile(request):
    user = request.user
    profile_obj, _ = Profile.objects.get_or_create(user=user)

    stats = {
        'posts_count': BlogPost.objects.filter(author=user).count(),
        'comments_count': Comment.objects.filter(author=user).count(),
        'likes_given': PostLike.objects.filter(user=user).count(),
        'ratings_given': PostRating.objects.filter(user=user).count(),
    }
    return render(request, 'blog/profile.html', {
        'profile': profile_obj,
        'stats': stats,
    })


@login_required
def edit_profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, 'blog/edit_profile.html', {'form': form})