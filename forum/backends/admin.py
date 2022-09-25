from django.contrib import admin

from .models import Thread, Post, User
# LOGIN - admin
# PASSWORD - admin
# Email - admin@admin.admin

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_editable = ('author',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'content', 'created_at', 'updated_at')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email', 'nickname')
    list_editable = ('name', 'surname', 'email', 'nickname')


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
