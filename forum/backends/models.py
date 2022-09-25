from django.db import models

class Thread(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    author = models.ForeignKey('User', on_delete=models.CASCADE, blank=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.CASCADE, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Content')
    created_at = models.DateField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateField(auto_now=True, verbose_name='Modified')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class User(models.Model):
    name = models.CharField(max_length=30, verbose_name='Name')
    surname = models.CharField(max_length=30, verbose_name='Surname')
    email = models.EmailField(max_length=50, verbose_name='Email')
    nickname = models.CharField(max_length=20, verbose_name='Nickname')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

