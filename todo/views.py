from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .models import TodoItem


def index(request):
    return TemplateResponse(request, "todo/index.html", {})


def todo_list(request):
    context = {
        "todo_count": TodoItem.objects.count(),
        "todo_list": TodoItem.objects.all(),
    }
    return TemplateResponse(request, "todo/list.html", context)


def todo_detail(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    return TemplateResponse(request, "todo/detail.html", {"todo": todo})
