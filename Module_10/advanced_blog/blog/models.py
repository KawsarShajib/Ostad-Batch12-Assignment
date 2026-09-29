from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name




class BlogPost(models.Model):
    
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
        )
    title = models.CharField(max_length=200)
    content = models.TextField()
    # content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # Explanation : 

    # (1) models.ForeignKey
    # ---------------------------------------------------------------------------------
    # an author/user (ONE) can make multiple posts (MANY). Remember that, a Foreign Key  
    # should always be on the MANY side of the database table/model. Hence we created the  
    # ForeignKey for an author/user in this BlogPost Model. 

    # (2) User
    # ---------
    # Django's built-in user model that was imported (from django.contrib.auth.models import User)
    # because here each registered/logged in user is an author of a post.

    # (3) on_delete=models.CASCADE
    # -----------------------------
    # CASCADE means the related blog posts will also be deleted.
    # if an author/user is deleted, all posts made by that user, will be deleted also.

    # on_delete=models.SET_NULL, Null = True
    # ---------------------------------------
    # Keep the blog posts but remove their author and set a Null value for the field

    # on_delete=models.PROTECT
    # --------------------------
    # Prevent deletion of the user if they still have related blog posts. 
    # So Django would essentially say: You can't delete this user because 
    # related BlogPost objects exist.

    # (4) related_name='blog_posts'
    # ------------------------------
    # It defines the reverse relationship name

    # post.author               : Who is the author of this post?
    # user.blog_posts.all()     : Give me all blog posts written by the author/user.

    # can be translated into plain English as:
    # ------------------------------------------
    # Create an author field in the BlogPost model that connects each blog post to one Django User. 
    # If that user is deleted, delete their related blog posts as well. From a User object, allow us 
    # to Reverse access all of that user's posts using user.blog_posts.all()

                    # BlogPost
                    # │
                    # │ author
                    # ↓
                    # User

                    # and because of:  related_name='blog_posts'

                    # BlogPost
                    # │
                    # │ author
                    # ↓
                    # User


#     title = models.CharField(max_length=200, db_index=True)
#     created_at = models.DateTimeField(db_index=True)

    # Relating the Category field to BlogPost model
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='posts'
    )
    # a post will be deleted if an user is deleted, hence on_delete=models.CASCADE,

    # Adding image field to BlogPost model
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    ) 

    # created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        # indexes = [
        #     models.Index(fields=['author', 'created_at']),
        #     models.Index(fields=['category', '-created_at']),
        # ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
# Use Database Indexes
# class BlogPost(models.Model):
#     title = models.CharField(max_length=200, db_index=True)
#     created_at = models.DateTimeField(db_index=True)
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['author', 'created_at']),
#             models.Index(fields=['category', '-created_at']),
#         ]

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # for replies
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    @property
    def is_reply(self):
        return self.parent is not None


class PostLike(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes comment {self.comment.id}'


class PostRating(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('post', 'user')  # One rating per user per post
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} rated {self.post.title}: {self.rating}'