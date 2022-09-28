from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Thread, Post, User
# LOGIN - admin
# PASSWORD - admin
# Email - admin@admin.admin

# class UserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'email', 'password')}),
#         (('Personal info'), {'fields': ('first_name', 'last_name')}),
#         (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                        'groups', 'user_permissions')}),
#         (('Important dates'), {'fields': ('last_login', 'date_joined')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'password1', 'password2')}
#         ),
#     )
#     form = UserChangeForm
#     add_form = UserCreationForm
#
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_editable = ('author',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'author', 'content', 'created_at', 'updated_at')

#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'surname', 'email', 'nickname')
#     list_editable = ('name', 'surname', 'email', 'nickname')

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
# admin.site.register(User, UserAdmin)
