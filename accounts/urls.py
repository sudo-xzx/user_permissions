from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("profile/", views.profile_edit, name="profile_edit"),

    path("management/users/", views.UserManagementListView.as_view(), name="user_management_list"),
    path("management/users/<int:pk>/", views.UserManagementDetailView.as_view(), name="user_management_detail"),
    path("management/users/<int:pk>/toggle-active/", views.user_toggle_active, name="user_toggle_active"),
    path("management/users/<int:pk>/set-group/", views.user_set_group, name="user_set_group"),
    path("management/users/<int:pk>/delete/", views.user_delete, name="user_delete"),
]
