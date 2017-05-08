from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile
import datetime
from django.contrib.auth.forms import PasswordResetForm

def UniqueEmailValidator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid username.')


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True)
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Not required'}),
        max_length=30,
        required=False,
        help_text='Optional field')
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Not required'}),
        max_length=30,
        required=False,
        help_text='Optional field')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['username'].validators.append(InvalidUsernameValidator)
        self.fields['username'].validators.append(ForbiddenUsernamesValidator)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_mame = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

    # проверка username без учета регистра, т.е. john и John учитываются как одно и то же имя пользователя + backend.py
    # setting.py = AUTHENTICATION_BACKENDS = ('accounts.backends.CaseInsensitiveModelBackend', )
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    description = forms.Textarea()
    phone = forms.IntegerField(
        required=False)
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),
                                      years=range(1980, datetime.datetime.now().year+1)),
        required=False)
    website = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=False)
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False)

    class Meta:
        model = UserProfile
        fields = ['phone', 'birth_date',
                  'role', 'website', 'city', 'description']

# Расширяем базовую форму PasswordResetForm для проверки наличия в БД введенного эмейла
# (добавляем метод clean_email)
# и добавляем в юрл url(r'^password_reset/$', auth_views.password_reset, ... строку:
#  'password_reset_form': MailCheckPasswordResetForm

from django.contrib.auth import get_user_model

class MailCheckPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254)

    error_messages = {
        'unknown': ("That email address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': ("The user account associated with this email "
                      "address cannot reset the password."),
        }

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = get_user_model()._default_manager.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == user.set_unusable_password())
            for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

