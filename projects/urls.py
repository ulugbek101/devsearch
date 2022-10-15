from django.urls import path

from . import views

urlpatterns = [
    path('', views.projects_view, name='projects'),
    path('project/<str:pk>/', views.project_view, name='project'),

    path('create-project/', views.project_create, name='project_create'),
    path('update-project/<str:pk>/', views.project_update, name='update_project'),
    path('delete-project/<str:pk>/', views.project_delete, name='delete_project'),

]
