from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.HelloWorld.as_view(), name='index'),
    path('api/users/', views.UserListView.as_view(), name='users'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/protected/', views.ProtectedView.as_view(), name='protected'),
    path('api/userprofile/', views.UserAccountView.as_view(), name="profile"),
    path('api/user-update/', views.UserProfileUpdateView.as_view(), name='user-update'),
    path('api/user-deactivate/', views.deactivate_user, name='user-deactivate'),
]
