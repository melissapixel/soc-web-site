from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserRegistrationForm, \
                    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html',
                            {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit=False)

            # Установить выбранный пароль
            new_user.set_password(                  # хеширует пароль перед его сохранением
            user_form.cleaned_data['password'])

            # Сохранить объект User
            new_user.save()

            # Создать профиль пользователя
            Profile.objects.create(user=new_user)

            return render(request,
                        'account/register_done.html',
                        {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                'account/register.html',
                {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        # для хранения данных во встроенной модели Юзер
        user_form = UserEditForm(instance=request.user,         # Заполнение формы текущими данными пользователя
                                data=request.POST)              # Проверить новые данные, которые прислал пользователь
        # для хранения дополнительных персональных данных
        profile_form = ProfileEditForm(instance=request.user.profile,
                                data=request.POST,
                                files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '\
                                    'successfully')

        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                'account/edit.html',
                {'user_form': user_form,
                'profile_form': profile_form})