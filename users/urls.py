from django.urls import path

from . import views

urlpatterns = [
    path('', views.users_view, name='profiles'),

    path('registration/', views.user_register, name='registration'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('account/', views.user_account, name='account'),

    path('profile/<str:pk>/', views.user_profile, name='profile'),
    path('profile-edit/', views.profile_edit, name='profile_edit'),

    path('skill-create/', views.skill_create, name='skill_create'),
    path('skill-update/<str:pk>/', views.skill_update, name='skill_update'),
    path('skill-delete/<str:pk>/', views.skill_delete, name='skill_delete'),

    path('inbox/', views.inbox_view, name='inbox'),
    path('message/<str:pk>/', views.message_view, name='message'),
    path('send-message/<str:pk>/', views.send_message, name='send_message'),
]
