from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    RegistrationForm,
    UserForm,
    ProfileForm
)

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse

from django.contrib.auth.models import User

from .models import Friend


# Create your views here.
def home(request):
    users = User.objects.exclude(id=request.user.id)
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        friends_request = Friend.who_added_user(user=request.user)
    except Friend.DoesNotExist:
        friends = None
    return render(request, 'accounts/home.html',
                  {'users': users, 'friends': friends, 'friends_request': friends_request}
                  )


# регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # form.save()

            # логинизация юреза после регистрации
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            user.set_password(password)
            user.save()
            from django.contrib.auth import authenticate, login
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            # логинизация юреза после регистрации

                    return redirect('/account')
    else:
        form = RegistrationForm()

    args = {'form': form}
    return render(request, 'accounts/reg_form.html', args)


# просмотр информации профиля
def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', {'user': user})


# редактирование профиля
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Your profile was successfully updated!')
            return render(request, 'accounts/profile.html', {'user': request.user})
        else:
            messages.add_message(request, messages.ERROR,
                                 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
        return render(request, 'accounts/settings/settings.html', {'user_form': user_form,
                                                                   'profile_form': profile_form}
                      )


# изменение пароля
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Данная функция принимает текущий запрос и обновлённый объект
            # пользователя из которого будет извлечён новый хэш сессии и соответственно обновляет хэш сессии
            # после смены пароля остаешься в системе
            messages.add_message(request, messages.SUCCESS,
                                 'Your password was successfully changed.')
            return redirect(reverse('account:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        return render(request, 'accounts/settings/password.html', {'form': form})

from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

def picture(request):
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fn = settings.MEDIA_ROOT + '/profile_pictures/' + \
             request.user.username + '.jpg'
        if os.path.isfile(fn):
            fs.delete(fn)
        filename = fs.save(fn, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'accounts/settings/picture.html', {
            'uploaded_file_url': uploaded_file_url, 'fn': fn
        })
    return render(request, 'accounts/settings/picture.html', )


def change_friends(request, operation, pk):
    new_friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, new_friend)
    elif operation == 'remove':
        Friend.remove_friend(request.user, new_friend)
    return redirect('account:home')

