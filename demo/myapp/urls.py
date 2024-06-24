from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact", views.contact, name="contact"),
    path("workouts/", views.todos, name="todos"),
    path("add/", views.add_todo, name="add_todo"),
    path("edit/<int:pk>/", views.edit_todo, name="edit_todo"),
    path("delete/<int:pk>/", views.delete_todo, name="delete_todo"),
    path("workouts/progress-graph/<int:pk>/", views.progress_graph, name="progress_graph"),
]