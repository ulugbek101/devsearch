from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegistrationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Skill, Message
from .utils import search_profiles, paginate_profiles


def users_view(request):
    profiles, search_query = search_profiles(request)
    profiles, custom_range = paginate_profiles(request, profiles, 6)
    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/profiles.html', context)


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has successfully created ! Log in to your account here.')
            return redirect('login')
        else:
            messages.error(request, 'Fields are filled incorrectly !')
            form = RegistrationForm(request.POST)
            context = {
                'form': form
            }
            return render(request, 'users/registration.html', context)

    form = RegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)


def user_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            full_name = user.profile.fullname
            messages.info(request, f'Welcome {full_name} !')
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or Password is incorrect !')
            return redirect('login')
    context = {}
    return render(request, 'users/login_register.html', context)


def user_logout(request):
    logout(request)
    messages.info(request, 'You have logged out !')
    return redirect('login')


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    dev_skills = profile.skill_set.exclude(description="")
    other_skills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'dev_skills': dev_skills,
        'other_skills': other_skills
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def user_account(request):
    account = request.user.profile
    context = {
        'account': account
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile has successfully updated !')
            return redirect('account')
        else:
            messages.error(request, 'Form filled incorrectly !')
            context = {
                'form': form
            }
            return render(request, 'users/form_template.html', context)
    form = ProfileForm(instance=profile)
    context = {
        'form': form
    }
    return render(request, 'users/form_template.html', context)


@login_required(login_url='login')
def skill_create(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill has successfully created !')
            return redirect('account')

    form = SkillForm()
    context = {
        'form': form
    }

    return render(request, 'users/form_template.html', context)


@login_required(login_url='login')
def skill_update(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.info(request, 'Skill has successfully updated !')
            return redirect('account')
    form = SkillForm(instance=skill)
    context = {
        'form': form
    }

    return render(request, 'users/form_template.html', context)


@login_required(login_url='login')
def skill_delete(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill has successfully deleted !')
        return redirect('account')
    context = {
        'obj': skill
    }
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox_view(request):
    profile = request.user.profile
    unread_messages = profile.messages.filter(is_read=False).count()

    context = {
        'profile': profile,
        'unread_messages': unread_messages,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def message_view(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    message.is_read = True
    message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)


def send_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.fullname = sender.fullname
                message.email = sender.email
            message.save()
            messages.success(request, 'Messages sent successfully !')
            return redirect('profile', pk=pk)

    form = MessageForm()
    context = {
        'form': form,

    }
    return render(request, 'users/send_message.html', context)
