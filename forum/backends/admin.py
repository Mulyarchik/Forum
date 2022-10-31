from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Question, Answer, Comment, User

# LOGIN - admin
# PASSWORD - admin
# Email - admin@admin.admin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
User._meta.get_field('email').required = True



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Important fields'), {'fields': ('email',)}),
    )

#@admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     #exclude = ('author',) # скрыть author поле, чтобы оно не отображалось в форме изменений
#
#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             obj.author = request.user.username
#         super().save_model(request, obj, form, change)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'author', 'created_at')
    list_editable = ('title', 'author')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'created_at')
    list_editable = ('content', 'author')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'author', 'created_at')
    list_editable = ('content', 'author')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_staff', 'image', )
    list_editable = ('is_staff', 'image',)


#admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)

