from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput

from .models import Question, Answer, CommentToAnswer


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    first_name = forms.CharField(
        label=("Name"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'text',
                                          'required': 'true',
                                          }))

    last_name = forms.CharField(
        label=("Surname"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'text',
                                          'required': 'true',
                                          }))
    username = forms.RegexField(
        label=("Username"), max_length=15, regex=r"^[\w.@+-]+$",
        help_text=("Required. 15 characters or fewer. Letters, digits and "
                   "@/./+/-/_ only."),
        error_messages={
            'invalid': ("This value may contain only letters, numbers and "
                        "@/./+/-/_ characters.")},
        widget=TextInput(attrs={'class': 'form-control',
                                'required': 'true',
                                })
    )

    email = forms.CharField(
        label=("Email"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'text',
                                          'required': 'true',
                                          'placeholder': 'for_example@mail.ru'
                                          }))
    password1 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'required': 'true',
                                          })
    )

    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'required': 'true',
                                          })
    )

    def email_clean(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label=("Username or Email"),
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'text',
                                      'required': 'true',
                                      }))
    password = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'password',
                                          'required': 'true',
                                          }))


class QuestionCreate(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'required': 'true',
        }))

    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'required': 'true',
        }))

    class Meta:
        model = Question
        exclude = ["author", "created_at"]
        fields = ("title", "content",)


class AnswerCreate(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'text',
            'required': 'true',
        })),

    class Meta:
        model = Answer
        exclude = ["author", "created_at"]
        fields = ("content",)
