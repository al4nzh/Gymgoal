from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact", views.contact, name="contact"),
    path("workouts/", views.todos, name="todos"),
    path("add/", views.add_todo, name="add_todo"),
    path("edit/<int:pk>/", views.edit_todo, name="edit_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
    path("workouts/progress-graph/<int:pk>/", views.progress_graph, name="progress_graph"),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='home'), name="logout"),
    path("register/", views.register, name="register"),
]