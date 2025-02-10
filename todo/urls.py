from django.urls import path

from . import views


app_name = "todo"
urlpatterns = [
    path("", views.todo_list, name="list"),
    path("new", views.todo_create, name="new"),
    path("count", views.todo_count, name="count"),
    path("new/title", views.title_check_new, name="title_check_new"),
    path("<int:todo_id>/", views.todo_detail, name="detail"),
    path("<int:todo_id>/edit", views.todo_edit, name="edit"),
    path("<int:todo_id>/title", views.title_check, name="title_check"),
]
