from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified ')

    def get_absolute_url(self):
        return "/thread/%i/" % self.id

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['-created_at']


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, verbose_name='question')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    def __str__(self):
        return self.content


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.content



# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='profile_picture', default='/media/profile_picture/defolt_user1.png')
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Profile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_picture', default='/media/profile_picture/defolt_user1.png', )
