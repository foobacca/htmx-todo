from django.views.generic import RedirectView
from django.urls import path

from . import views


app_name = "todo"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="todo:list", permanent=False)),
    path("list/", views.todo_list, name="list"),
    path("<int:todo_id>/", views.todo_detail, name="detail"),
]
