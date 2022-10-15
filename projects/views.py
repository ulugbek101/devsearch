from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProjectForm, ReviewForm
from .models import Project, Tag, Review
from .utils import search_projects, paginate_projects


def projects_view(request):
    projects, search_query = search_projects(request)
    projects, custom_range = paginate_projects(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project_view(request, pk):
    form = ReviewForm()
    project = Project.objects.get(id=pk)

    try:
        profile = request.user.profile
    except:
        profile = None

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user.profile
            form.project = project
            form.save()
            messages.success(request, "Project has reviewed successfully !")
            return redirect('project', pk=project.id)

    try:
        vote = project.vote_set.values().get(profile_id=profile.id).get('vote')  # checking weter user liked or disliked a project
        vote = bool(vote)
    except:
        vote = None

    context = {
        'vote': vote,
        'project': project,
        'form': form,
        'likes': project.vote_set.filter(vote=1).count(),
        'dislikes': project.vote_set.filter(vote=0).count(),
    }

    return render(request, 'projects/project.html', context)


@login_required(login_url='login')
def project_create(request):
    profile = request.user.profile
    if request.method == 'POST':
        # newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            # for tag in newtags:
            #     tag, created = Tag.objects.get_or_create(name=tag)
            #     project.tags.add(tag)
            #
            messages.success(request, 'Project has been created, please add tags for a project !')
            return redirect('update_project', pk=project.id)
    form = ProjectForm()
    context = {
        'form': form,
        'project_create': True
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def project_update(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for newtag in newtags:
                tag, created = Tag.objects.get_or_create(name=newtag)
                project.tags.add(tag)
            messages.success(request, 'Project has been successfully updated !')
            return redirect('account')
        else:
            form = ProjectForm(instance=project)
            context = {
                'form': form,
                'project': project,
            }
            messages.error(request, 'Form filled incorrectly !')
            return render(request, 'projects/project_form.html', context)
    form = ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def project_delete(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project has been successfully deleted !')
        return redirect('account')
    context = {
        'obj': project
    }
    return render(request, 'delete_template.html', context)
