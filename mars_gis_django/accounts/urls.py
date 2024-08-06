from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from . import views
# from .views import CreateProject
# from .views import HomeView, OrganizationHomeView
# from .views import HomeView, OrganizationHomeView
# from accounts.views import SignUp

app_name = 'accounts'
urlpatterns = [
    path('home/', views.users_home, name='home'),
    # path('project/form/', views.CreateProject.as_view(), name='create_project'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/join/', views.join_project, name='join_project'),
    # path('home_tmp/', HomeView.as_view(), name='home_tmp'),
    # path('org/<int:org_id>/home/', OrganizationHomeView.as_view(), name='org_home'),
]
