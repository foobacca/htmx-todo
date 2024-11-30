from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from .forms import TodoForm
from .models import TodoItem


def index(request):
    return TemplateResponse(request, "todo/index.html", {})


def todo_list(request):
    messages = []
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save()
            messages.append(f"Created new todo item: {new_todo.id}, {new_todo.title}")
            # finally, reset the form for redisplay
            form = TodoForm()
        # if form is not valid, leave it with errors for redisplay
    else:
        form = TodoForm()
    context = {
        "todo_count": TodoItem.objects.count(),
        "todo_list": TodoItem.objects.all(),
        "form": form,
        "messages": messages,
    }
    return TemplateResponse(request, "todo/list.html", context)


def todo_detail(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    return TemplateResponse(request, "todo/detail.html", {"todo": todo})
