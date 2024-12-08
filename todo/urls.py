from django.urls import path

from . import views


app_name = "todo"
urlpatterns = [
    path("", views.todo_list, name="list"),
    path("new", views.todo_create, name="new"),
    path("<int:todo_id>/", views.todo_detail, name="detail"),
    path("<int:todo_id>/edit", views.todo_edit, name="edit"),
]
