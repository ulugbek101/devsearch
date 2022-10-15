from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('projects/', views.get_projects),
    path('projects/<str:pk>/', views.get_project),

    path('add-tag/', views.add_tag),
    path('remove-tag/', views.remove_tag),
    
    path('remove-message/', views.remove_message),
    path('vote/', views.vote_project),
]
