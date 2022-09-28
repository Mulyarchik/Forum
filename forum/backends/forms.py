from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput


# from django.core.exceptions import ValidationError

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='First Name')

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
