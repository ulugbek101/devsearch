from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from projects.models import Project, Tag, Vote
from users.models import Message, Profile
from .serializers import ProfileSerializer, ProjectSerializer, TagSerializer, MessageSerializer


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def remove_tag(request):
    tag_id = request.data['tag']
    project_id = request.data['project']

    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)

    project.tags.remove(tag)

    return Response('Tag was deleted !')


@api_view(['POST'])
def add_tag(request):
    project_id = request.data['project']
    tag_name = request.data['tag'].lower().replace(",", " ").strip()

    project = Project.objects.get(id=project_id)
    tag, created = project.tags.get_or_create(name=tag_name)
    project.tags.add()
    if created:
        tag = TagSerializer(tag, many=False)
        project = ProjectSerializer(project, many=False)
        return Response({
            "tag": tag.data,
            "project": project.data,
        })
    else:
        return Response("Tag already exists !")


@api_view(['DELETE'])
def remove_message(request):
    deleting_messages = request.data['messages']
    owner_id = request.data['profile']
    profile = ProfileSerializer(Profile.objects.get(id=owner_id), many=False)
    all_messages = MessageSerializer(Message.objects.filter(recipient__id=owner_id), many=True)
    for item in deleting_messages:
        msg = Message.objects.get(id=item)
        msg.delete()
    
    data = {
        'profile': profile.data,
        'all_messages': all_messages.data,
    }
    return Response( data )


@api_view(['PUT'])
def vote_project(request):

    value, profile_id, project_id = [item for item in request.data.values()]
    value = 1 if value == 'like' else 0
    project = Project.objects.get(id=project_id)
    profile = Profile.objects.get(id=profile_id)

    def create_vote(user_profile, user_project, user_value):
        created_vote = Vote.objects.create(
            vote=user_value,
            project=user_project,
            profile=user_profile
        )
        created_vote.save()
    try:
        create_vote(profile, project, value)
    except:
        vote = Vote.objects.get(profile=profile, project=project)
        vote.delete()
        create_vote(profile, project, value)

    data = {
        'is_liked': True if value == 1 else False,
        # 'is_disliked': True if value == 0 else False,
        "likes": project.vote_set.filter(vote=1).count(),
        "dislikes": project.vote_set.filter(vote=0).count(),
    }
    return Response(data)
