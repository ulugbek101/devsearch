from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Skill, Profile
from projects.models import Tag, Project


def search_profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(title__icontains=search_query)
    profiles = Profile.objects.filter(~Q(bio=None) &
                                      ~Q(short_intro=None) &
                                      ~Q(location=None) &
                                      ~Q(bio="") &
                                      ~Q(short_intro="") &
                                      ~Q(location=""))
    profiles = profiles.distinct().filter(Q(fullname__icontains=search_query) |
                                          Q(short_intro__icontains=search_query) |
                                          Q(skill__in=skills)
                                          )
    return profiles, search_query


def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = int(page) - 2 if int(page) - 2 > 0 else 1
    right_index = int(page) + 2 if int(page) + 2 <= paginator.num_pages else paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return profiles, custom_range
