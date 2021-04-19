from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.views.generic import UpdateView
from accounts.forms import UserUpdateForm, ProfileFormset
# LoginRequiredMixin добавляет проверку того, что пользователь авторизован в системе
from accounts.models import User
from posts.models import Apartment


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/user_update.html'
    # отвечает за импорт модели пользователя
    model = get_user_model()
    form_class = UserUpdateForm
    success_url = '/'
    login_url = '/admin/login'

    def get_object(self, queryset=None):
        return self.request.user


def update_profile_view(request):
    if request.method == 'POST':
        formset = ProfileFormset(request.POST, request.FILES, instance=request.user)
        if formset.is_valid():
            profile = formset.save()
            print(profile)
        print(formset.errors)
    else:
        formset = ProfileFormset()
    return render(request, 'profile_update.html', {'formset': formset})


@login_required
def personal(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileFormset(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            profile.save()
            return redirect('register-professional')
    else:
        form = ProfileFormset(instance=profile)
    return render(request, 'accounts/user-update.html', {
        'form': form
    })


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='common_users'))