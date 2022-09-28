from django.contrib import admin

from .models import Thread, Post


# LOGIN - admin
# PASSWORD - admin
# Email - admin@admin.admin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_editable = ('author',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'content', 'created_at', 'updated_at')


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(User, UserAdmin)
