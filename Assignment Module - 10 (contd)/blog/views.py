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

# Bad
# ----------------------------------------------------------------
# posts = BlogPost.objects.all()
# for post in posts:
#     print(post.author.username)   # Extra query for every post

# Good and Fast
# ---------------------------------------------------------------
# posts = BlogPost.objects.select_related('author', 'category')

# Important Tips
# --------------
# Use distinct=True with Count() when joining multiple tables to avoid wrong counts.
# Use select_related() / prefetch_related() together with annotate() for better performance.
# You can filter after annotating:

# Example : Posts that have more than 10 likes
#       popular = BlogPost.objects.annotate(
#           like_count=Count('likes')
#       ).filter(like_count__gt=10)


# Use select_related() when the relationship is many-to-one or one-to-one 
# (e.g. BlogPost → Author, BlogPost → Category).
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



    # Use annotate() instead of Python loops
    # -----------------------------------------------------------
    # Python# Bad (slow)
    # -----------------------------------------------------------
    # for post in posts:
    #     post.like_count = post.likes.count()       # Query per post
    #     post.avg_rating = post.ratings.aggregate(Avg('rating'))

    # Good (fast)
    # -----------------------------------------------------------
    # posts = BlogPost.objects.annotate(
    #     like_count=Count('likes', distinct=True),
    #     comment_count=Count('comments', distinct=True),
    #     avg_rating=Avg('ratings__rating')
    # )






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


    # ==================================================================================================
    # Prefetch top-level comments + their replies + likes
    # ==================================================================================================
    # Bad
    # ------------------------------------------------------------------
    # posts = BlogPost.objects.all()
    # for post in posts:
    #     print(post.comments.count())   # Extra query per post

    # Good
    # ------------------------------------------------------------------
    # posts = BlogPost.objects.prefetch_related('comments', 'likes', 'ratings')

    # For nested data (comments + replies):
    # --------------------------------------------------
    # comments = Comment.objects.filter(post=post, parent=None).prefetch_related(
    #     Prefetch('replies', queryset=Comment.objects.select_related('author'))
    # )

    # Use select_related()      for ==> ForeignKey / OneToOne and 
    # Use prefetch_related()    for ==> Reverse ForeignKey / ManyToMany
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
        # 'category': Category,
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
    return render(request, 'blog/my_posts.html', {
        'posts': posts,
        'posts_count': posts.count(),
    })




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

    return render(request, 'blog/popular_posts.html', {
        'posts': posts,
        'posts_count': posts.count(),
    })







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












# =============================================================================================================
# GUIDELINES : Practical guides to Django ORM Performance Tips.
# =============================================================================================================

# -----------------------------------------------------
# 1. Use select_related() for ForeignKey / OneToOne
# -----------------------------------------------------

# # Bad
# posts = BlogPost.objects.all()
# for post in posts:
#     print(post.author.username)   # Extra query for every post

# # Good
# posts = BlogPost.objects.select_related('author', 'category')



# # Use select_related() when the relationship is many-to-one or 
# # one-to-one (e.g. BlogPost → Author, BlogPost → Category).


# --------------------------------------------------------------
# 2. Use prefetch_related() for Reverse ForeignKey / ManyToMany
# --------------------------------------------------------------

# # Bad
# posts = BlogPost.objects.all()
# for post in posts:
#     print(post.comments.count())   # Extra query per post

# # Good
# posts = BlogPost.objects.prefetch_related('comments', 'likes', 'ratings')

# For nested data (comments + replies):
# --------------------------------------
# from django.db.models import Prefetch

# comments = Comment.objects.filter(post=post, parent=None).prefetch_related(
#     Prefetch('replies', queryset=Comment.objects.select_related('author'))
# )


# ------------------------------------------
# 3. Use annotate() instead of Python loops
# ------------------------------------------

# # Bad (slow)
# for post in posts:
#     post.like_count = post.likes.count()       # Query per post
#     post.avg_rating = post.ratings.aggregate(Avg('rating'))

# # Good (fast)
# posts = BlogPost.objects.annotate(
#     like_count=Count('likes', distinct=True),
#     comment_count=Count('comments', distinct=True),
#     avg_rating=Avg('ratings__rating')
# )


# ------------------------------
# 4. Avoid count() inside loops
# ------------------------------

# # Bad
# if post.comments.count() > 0: ...

# # Good
# posts = BlogPost.objects.annotate(comment_count=Count('comments'))
# if post.comment_count > 0: ...



# ------------------------------------------------
# 5. Use only() and defer() to fetch fewer fields
# ------------------------------------------------

# # Only fetch needed columns
# posts = BlogPost.objects.only('title', 'created_at', 'author_id')

# # Opposite: fetch everything except large fields
# posts = BlogPost.objects.defer('content')


# ----------------------------------------------------------
# 6. Use exists() instead of count() or boolean conversion
# ----------------------------------------------------------

# # Bad
# if PostLike.objects.filter(post=post, user=user).count() > 0:

# # Bad
# if PostLike.objects.filter(post=post, user=user):

# # Good
# if PostLike.objects.filter(post=post, user=user).exists():


# -------------------------
# 7. Add Database Indexes
# -------------------------

# class BlogPost(models.Model):
#     title = models.CharField(max_length=200, db_index=True)
#     created_at = models.DateTimeField(db_index=True)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['author', 'created_at']),
#             models.Index(fields=['category', '-created_at']),
#         ]
# -------------        
# Also useful:
# -------------
# class PostLike(models.Model):
#     class Meta:
#         unique_together = ('post', 'user')   # automatically creates index



# -----------------------------------
# 8. Don’t fetch data you don’t need
# -----------------------------------

# # Bad
# posts = BlogPost.objects.all()   # loads everything

# # Better
# posts = BlogPost.objects.all()[:20]   # limit results

# # Use pagination for large lists.



# ---------------------------------------------------------
# 9. Combine select_related + prefetch_related + annotate
# ---------------------------------------------------------

# # Best practice for home and post_detail pages:
    
# posts = BlogPost.objects.select_related(
#     'author', 'category'
# ).prefetch_related(
#     'likes', 'comments'
# ).annotate(
#     like_count=Count('likes', distinct=True),
#     comment_count=Count('comments', distinct=True),
#     avg_rating=Avg('ratings__rating')
# ).order_by('-created_at')



# --------------------------------------------
# 10. Use iterator() for very large querysets
# --------------------------------------------

# # Saves memory when processing thousands of rows
# for post in BlogPost.objects.all().iterator():
#     process(post)



# ============================================================================================================
# Common N+1 Problem in a Project
# ============================================================================================================
# Situation                   Wrong                                   Correct
# ============================================================================================================
# Show author name            post.author.username                    select_related('author')
# Show category name          post.category.name                      select_related('category')
# Show comments               post.comments.all()                     prefetch_related('comments')
# Show like count             post.likes.count()                      annotate(like_count=Count('likes'))
# Show replies of comments    Loop + query                            Prefetch('replies', ...)
# ============================================================================================================






# =============================================================================================================
# What is  Django ORM aggregation ?
# =============================================================================================================
# Aggregation means calculating a single summary value from multiple rows 
# (like count, total, average, minimum, maximum, etc.).

# In Django, we use the django.db.models functions:

# from django.db.models import Count, Avg, Sum, Min, Max

# ---------------------------------------------
# 1. Count()
# ---------------------------------------------
# # How many likes does each post have?
# posts = BlogPost.objects.annotate(
#     like_count=Count('likes')
# )

# # How many comments?
# posts = BlogPost.objects.annotate(
#     comment_count=Count('comments')
# )

# # How many posts has a user written?
# user_posts = BlogPost.objects.filter(author=user).count()

# like_count=Count('likes', distinct=True)
# comment_count=Count('comments', distinct=True)


# ---------------------------------------------
# 2. Avg()
# ---------------------------------------------
# # Average rating of a post
# posts = BlogPost.objects.annotate(
#     avg_rating=Avg('ratings__rating')
# )
# Example result: 4.3

# 3. Sum()

# # Total of all ratings given by a user
# total = PostRating.objects.filter(user=user).aggregate(
#     total=Sum('rating')
# )

# ---------------------------------------------
# 4. Min() and Max()
# ---------------------------------------------
# # Finds the lowest / highest value.
# stats = PostRating.objects.filter(post=post).aggregate(
#     min_rating=Min('rating'),
#     max_rating=Max('rating')
# )





# =============================================================================================================
# annotate() vs aggregate()
# =============================================================================================================
# Method          What it does                            Returns             Use Case
# ------------------------------------------------------------------------------------------------------------------
# annotate()      Adds calculated field to each object    QuerySet            Show like_count on every post
# aggregate()     Calculates one summary value            Dictionary          Total comments of the whole site
# ------------------------------------------------------------------------------------------------------------------

# Example of annotate():

# posts = BlogPost.objects.annotate(
#     like_count=Count('likes'),
#     comment_count=Count('comments'),
#     avg_rating=Avg('ratings__rating')
# )
# # Now every post has: post.like_count, post.comment_count, post.avg_rating

# Example of aggregate():
# ------------------------------------------
# from django.db.models import Count, Avg

# stats = BlogPost.objects.aggregate(
#     total_posts=Count('id'),
#     total_likes=Count('likes'),
#     average_rating=Avg('ratings__rating')
# )

# Result: {'total_posts': 25, 'total_likes': 340, 'average_rating': 4.2}

# Examples : 
# ------------------------------------------
# Home page - show stats for every post

# posts = BlogPost.objects.select_related('author').annotate(
#     like_count=Count('likes', distinct=True),
#     comment_count=Count('comments', distinct=True),
#     avg_rating=Avg('ratings__rating'),
#     rating_count=Count('ratings', distinct=True),
# )

# Popular posts - order by engagement

# posts = BlogPost.objects.annotate(
#     like_count=Count('likes', distinct=True),
#     comment_count=Count('comments', distinct=True),
#     avg_rating=Avg('ratings__rating'),
#     engagement=Count('likes') + Count('comments')
# ).order_by('-engagement', '-avg_rating')

# Important Tips
#     --------------------------------------------------------------------------------------------
#     Use distinct=True with Count() when joining multiple tables to avoid wrong counts.
#     Use select_related() / prefetch_related() together with annotate() for better performance.
#     --------------------------------------------------------------------------------------------

# You can filter after annotating:

# Posts that have more than 10 likes
#       popular = BlogPost.objects.annotate(
#           like_count=Count('likes')
#       ).filter(like_count__gt=10)

# --------------
# Summary Table
# -----------------------------------------------------------------------------------------
# Function                Purpose                             Example
# -----------------------------------------------------------------------------------------
# Count                   Number of items                     Total likes, total comments
# Avg                     Average value                       Average star rating
# Sum                     Total of values                     Sum of all ratings
# Min                     Smallest value                      Lowest rating
# Max                     Largest value                       Highest rating
# -----------------------------------------------------------------------------------------