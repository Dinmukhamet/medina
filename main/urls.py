from django.urls import include, path
from main import views

urlpatterns = [
    path('projects/', views.ListProjectsView.as_view(), name='list_projects'),
    path('projects/<int:pk>/', views.RetrieveProjectView.as_view(), name='retrieve_project'),
    path('projects/create/', views.CreateProjectView.as_view(), name='create_project')
]