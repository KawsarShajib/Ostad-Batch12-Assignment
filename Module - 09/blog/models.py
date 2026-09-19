from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# for use of profile picture functionality
from django.db.models.signals import post_save
from django.dispatch import receiver


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})







class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png',
        blank=True
    )

    def __str__(self):
        return f'{self.user.username} Profile'


# Automatically create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


