# from django.contrib import admin
# from .models import BlogPost, Profile


# @admin.register(BlogPost)
# class BlogPostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'created_at', 'updated_at')
#     list_filter = ('created_at', 'author')
#     search_fields = ('title', 'content')
#     date_hierarchy = 'created_at'



# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'bio')



from django.contrib import admin
from .models import BlogPost, Profile, Comment, PostLike, CommentLike, PostRating


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'get_like_count', 'get_comment_count', 'get_avg_rating')
    list_filter = ('created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author',)

    def get_like_count(self, obj):
        return obj.likes.count()
    get_like_count.short_description = 'Likes'

    def get_comment_count(self, obj):
        return obj.comments.count()
    get_comment_count.short_description = 'Comments'

    def get_avg_rating(self, obj):
        from django.db.models import Avg
        avg = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else '—'
    get_avg_rating.short_description = 'Avg Rating'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_at', 'short_content')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('post', 'author', 'parent')

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('post', 'user')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('comment', 'user')


@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    raw_id_fields = ('post', 'user')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')
    