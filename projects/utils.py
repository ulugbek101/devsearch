from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from projects.models import Tag, Project


def search_projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(tags__in=tags) |
        Q(owner__fullname__icontains=search_query)
    )

    return projects, search_query


def paginate_projects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = int(page) - 2 if int(page) - 2 > 0 else 1
    right_index = int(page) + 2 if int(page) + 2 <= paginator.num_pages else paginator.num_pages

    custom_range = range(left_index, right_index + 1)

    return projects, custom_range
