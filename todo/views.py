from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods, require_safe

from .forms import TodoForm
from .models import TodoItem


@require_safe
def todo_list(request):
    if search := request.GET.get("q", ""):
        todo_qs = TodoItem.objects.contains_text(search)
    else:
        todo_qs = TodoItem.objects.all()

    context = {
        "todo_count": todo_qs.count(),
        "todo_list": todo_qs,
        "search_term": search,
    }
    return TemplateResponse(request, "todo/list.html", context)


@require_safe
def todo_detail(request, todo_id: int):
    todo = get_object_or_404(TodoItem, id=todo_id)
    return TemplateResponse(request, "todo/detail.html", {"todo": todo})


@require_http_methods(["GET", "HEAD", "POST"])
def todo_create(request):
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
    pass


@require_http_methods(["GET", "HEAD", "POST"])
def todo_edit(request, todo_id: int):
    messages = []
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            # TODO: update existing item
            new_todo = form.save()
            messages.append(f"Created new todo item: {new_todo.id}, {new_todo.title}")
            # finally, reset the form for redisplay
            form = TodoForm()
        # if form is not valid, leave it with errors for redisplay
    else:
        form = TodoForm()
    pass


def todo_delete(request):
    pass
