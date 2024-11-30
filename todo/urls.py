from django.urls import path

from . import views


app_name = "todo"
urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.todo_list, name="list"),
    path("<int:todo_id>/", views.todo_detail, name="detail"),
]
